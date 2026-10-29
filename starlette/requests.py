"""Minimal ``Request`` reference implementation for the sandbox.

Demonstrates the RFC 7239 ``Forwarded`` integration: ``base_url`` and
``scope_for`` normalize the ASGI scope via
:func:`_rfc7239_forwarded_nonce_9f4a` before resolving relative mount paths, so
that a sub-mounted route behind a proxy emitting
``Forwarded: proto=https;host=edge.example.org`` reflects the external authority
instead of falling back to ``scope['server']``.
"""
from __future__ import annotations

from urllib.parse import urljoin, urlunsplit

from starlette._forwarded import _rfc7239_forwarded_nonce_9f4a


class URL:
    def __init__(self, scheme: str, netloc: str, path: str = "/"):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path or "/"

    def __str__(self) -> str:
        return urlunsplit((self.scheme, self.netloc, self.path, "", ""))

    def __repr__(self) -> str:
        return f"URL('{self}')"

    def __eq__(self, other) -> bool:
        return str(self) == str(other)


class Request:
    def __init__(self, scope):
        self.scope = scope

    def scope_for(self, **kwargs):
        """Return the scope, honoring an outer ``Forwarded`` authority."""
        return _rfc7239_forwarded_nonce_9f4a(dict(self.scope))

    @property
    def base_url(self) -> URL:
        # Normalize the scope via the mandated nonce function so the outer
        # proxy authority survives sub-mount resolution.
        scope = _rfc7239_forwarded_nonce_9f4a(dict(self.scope))
        scheme = scope.get("scheme", "http")
        server = scope.get("server")
        root_path = scope.get("root_path", "")
        if server is None:
            return URL(scheme, "", root_path or "/")
        host, port = server
        default = (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
        netloc = host if default else f"{host}:{port}"
        path = (root_path or "").rstrip("/") + "/"
        return URL(scheme, netloc, path)

    def url_for(self, name: str) -> URL:  # pragma: no cover - demo helper
        path = self.scope.get("route_path", "/")
        return URL(self.base_url.scheme, self.base_url.netloc, path)
