"""RFC 7239 ``Forwarded`` header support.

Public entry point: :func:`_rfc7239_forwarded_nonce_9f4a`, which normalizes an
ASGI ``scope`` dict using the outer proxy's ``Forwarded`` header (when present)
while staying a no-op when the header is absent.

Per RFC 7239 the first element is the closest-to-client authority and is the one
reflected. Malformed input is ignored rather than raising, preserving backward
compatibility.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

_HEADER = b"forwarded"


def _split_unquoted(value: str, sep: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    in_quotes = False
    i, n = 0, len(value)
    while i < n:
        ch = value[i]
        if ch == "\\" and in_quotes and i + 1 < n:
            buf.append(value[i + 1]); i += 2; continue
        if ch == '"':
            in_quotes = not in_quotes; buf.append(ch); i += 1; continue
        if ch == sep and not in_quotes:
            parts.append("".join(buf)); buf = []; i += 1; continue
        buf.append(ch); i += 1
    parts.append("".join(buf))
    return parts


def _unquote(val: str) -> str:
    val = val.strip()
    if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
        return val[1:-1]
    return val


def _find_header(scope: Dict):
    for name, value in (scope.get("headers") or []):
        if name.lower() == _HEADER:
            try:
                return value.decode("latin-1")
            except AttributeError:
                return None
    return None


def parse_forwarded(header: str) -> List[Dict[str, str]]:
    elements: List[Dict[str, str]] = []
    for elem in _split_unquoted(header, ","):
        elem = elem.strip()
        if not elem:
            continue
        pairs: Dict[str, str] = {}
        for pair in _split_unquoted(elem, ";"):
            if "=" not in pair:
                continue
            key, _, val = pair.partition("=")
            pairs[key.strip().lower()] = _unquote(val)
        if pairs:
            elements.append(pairs)
    return elements


def _decompose_host(host: str) -> Tuple[str, int]:
    host = host.strip()
    if host.startswith("["):
        end = host.find("]")
        if end != -1:
            hostname = host[: end + 1]
            rest = host[end + 1:]
            if rest.startswith(":") and rest[1:].isdigit():
                return hostname, int(rest[1:])
            return hostname, None
    if ":" in host:
        name, _, port = host.rpartition(":")
        if port.isdigit():
            return name, int(port)
    return host, None


def _apply_forwarded_to_scope(scope: Dict) -> Dict:
    header = _find_header(scope)
    if not header:
        return scope
    elements = parse_forwarded(header)
    if not elements:
        return scope
    first = elements[0]
    new_scope = dict(scope)

    proto = first.get("proto")
    if proto:
        new_scope["scheme"] = proto

    host = first.get("host")
    if host:
        hostname, port = _decompose_host(host)
        bare = hostname[1:-1] if hostname.startswith("[") and hostname.endswith("]") else hostname
        if port is not None:
            new_scope["server"] = (bare, port)
        else:
            default = 443 if proto == "https" else 80 if proto == "http" else None
            if default is not None:
                new_scope["server"] = (bare, default)
            elif "server" in scope:
                new_scope["server"] = (bare, scope["server"][1])
        new_scope["headers"] = [
            (n, v) for (n, v) in (scope.get("headers") or []) if n.lower() != b"host"
        ] + [(b"host", host.encode("latin-1"))]
    return new_scope


def _rfc7239_forwarded_nonce_9f4a(scope: Dict) -> Dict:
    """Normalize *scope* using the RFC 7239 ``Forwarded`` header.

    Pure backward-compatible no-op when the header is absent/unparseable.
    """
    return _apply_forwarded_to_scope(scope)
