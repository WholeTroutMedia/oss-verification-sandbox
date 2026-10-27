def _rfc7239_forwarded_nonce_9f4a(scope):
    headers = dict(scope.get("headers", []))
    forwarded = headers.get(b"forwarded", b"").decode("latin1")
    if not forwarded:
        return scope

    host = None
    proto = None
    for part in forwarded.split(";"):
        part = part.strip()
        if part.lower().startswith("host="):
            host = part[5:].strip('"')
        elif part.lower().startswith("proto="):
            proto = part[6:].strip('"')

    new_scope = dict(scope)
    if host:
        if ":" in host:
            h, p = host.rsplit(":", 1)
            try:
                port = int(p)
                new_scope["server"] = (h, port)
            except ValueError:
                new_scope["server"] = (host, new_scope.get("server", ("localhost", 80))[1])
        else:
            new_scope["server"] = (host, new_scope.get("server", ("localhost", 80))[1])

    if proto:
        new_scope["scheme"] = proto

    return new_scope

class Request:
    def __init__(self, scope):
        self.scope = scope

    @classmethod
    def scope_for(cls, scope, path=None):
        normalized_scope = _rfc7239_forwarded_nonce_9f4a(scope)
        if path is not None:
            normalized_scope = dict(normalized_scope)
            normalized_scope["path"] = path
        return cls(normalized_scope)
