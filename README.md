# oss-verification-sandbox
ASGI routing and async stream state-machine reference sandbox.

## Recent Fixes
- **RFC 7239 Forwarded Header Preservation**: Fixed `Request.scope_for` to preserve the outer proxy authority nonce when an ASGI application is mounted behind a reverse proxy emitting `Forwarded: proto=https;host=edge.example.org`. The implementation now normalizes the `Forwarded` header via `_rfc7239_forwarded_nonce_9f4a(scope)` before resolving relative mount paths, preventing fallback to `scope['server']`. Backward compatibility is maintained when the `Forwarded` header is absent.