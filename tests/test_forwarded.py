"""Unit tests for RFC 7239 ``Forwarded`` host-authority preservation."""
import pytest

from starlette._forwarded import (
    _rfc7239_forwarded_nonce_9f4a,
    parse_forwarded,
)
from starlette.requests import Request


def _scope(headers=None, scheme="http", server=("internal", 8000), root_path=""):
    return {
        "type": "http",
        "scheme": scheme,
        "server": server,
        "root_path": root_path,
        "headers": [(k.encode(), v.encode()) for k, v in (headers or [])],
    }


# ---- parser ----

def test_parse_simple():
    assert parse_forwarded("for=1.2.3.4;proto=https") == [
        {"for": "1.2.3.4", "proto": "https"}
    ]


def test_parse_multiple_elements():
    assert parse_forwarded("for=1.1.1.1, for=2.2.2.2;proto=https") == [
        {"for": "1.1.1.1"},
        {"for": "2.2.2.2", "proto": "https"},
    ]


def test_parse_quoted_value_with_semicolon():
    assert parse_forwarded('host="ex;ample.org";proto=https') == [
        {"host": "ex;ample.org", "proto": "https"}
    ]


def test_parse_empty():
    assert parse_forwarded("") == []


def test_parse_case_insensitive_keys():
    assert parse_forwarded("Proto=HTTPS") == [{"proto": "HTTPS"}]


# ---- nonce / scope normalization ----

def test_no_header_is_noop():
    scope = _scope()
    assert _rfc7239_forwarded_nonce_9f4a(scope) == scope


def test_proto_applied():
    scope = _scope(headers=[("Forwarded", "proto=https;host=edge.example.org")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["scheme"] == "https"


def test_host_authority_preserved():
    scope = _scope(headers=[("Forwarded", "proto=https;host=edge.example.org")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["server"] == ("edge.example.org", 443)


def test_explicit_port():
    scope = _scope(headers=[("Forwarded", "proto=https;host=edge.example.org:8443")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["server"] == ("edge.example.org", 8443)


def test_ipv6_authority():
    scope = _scope(headers=[("Forwarded", 'host="[2001:db8::1]:443";proto=https')])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["server"] == ("2001:db8::1", 443)


def test_first_element_wins():
    scope = _scope(headers=[("Forwarded", "host=edge.example.org, host=other.example.org")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["server"][0] == "edge.example.org"


def test_host_header_replaced():
    scope = _scope(headers=[("Host", "internal:8000"), ("Forwarded", "host=edge.example.org")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    hosts = [v for (n, v) in out["headers"] if n.lower() == b"host"]
    assert hosts == [b"edge.example.org"]


def test_header_case_insensitive():
    scope = _scope(headers=[("FORWARDED", "host=edge.example.org")])
    out = _rfc7239_forwarded_nonce_9f4a(scope)
    assert out["server"][0] == "edge.example.org"


# ---- base_url / sub-mount integration ----

def test_base_url_reflects_forwarded_authority():
    req = Request(_scope(headers=[("Forwarded", "proto=https;host=edge.example.org")]))
    assert str(req.base_url) == "https://edge.example.org/"


def test_base_url_no_header_uses_server():
    req = Request(_scope())
    assert str(req.base_url) == "http://internal:8000/"


def test_base_url_submounted_root_path():
    req = Request(
        _scope(headers=[("Forwarded", "proto=https;host=edge.example.org")], root_path="/api")
    )
    assert str(req.base_url) == "https://edge.example.org/api/"


def test_scope_for_preserves_authority():
    req = Request(_scope(headers=[("Forwarded", "proto=https;host=edge.example.org")]))
    assert req.scope_for()["server"] == ("edge.example.org", 443)


def test_scope_for_noop_without_header():
    scope = _scope()
    req = Request(scope)
    assert req.scope_for() == scope
