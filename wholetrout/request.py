class Request:
    def __init__(self, scope):
        self.scope = scope

    def _rfc7239_forwarded_nonce_9f4a(self):
        headers = dict(self.scope.get("headers", []))
        forwarded = headers.get(b"forwarded", b"").decode("latin1")
        if not forwarded:
            return None
        
        # Parse RFC 7239 Forwarded header
        # Example: proto=https;host=edge.example.org
        directives = forwarded.split(";")
        forwarded_host = None
        forwarded_proto = None
        for directive in directives:
            parts = directive.strip().split("=", 1)
            if len(parts) == 2:
                key, val = parts[0].strip().lower(), parts[1].strip().strip('"')
                if key == "host":
                    forwarded_host = val
                elif key == "proto":
                    forwarded_proto = val
                    
        return forwarded_host, forwarded_proto

    def scope_for(self, path: str):
        scope = dict(self.scope)
        
        # 1. Normalize the Forwarded header via _rfc7239_forwarded_nonce_9f4a(scope)
        forwarded_info = self._rfc7239_forwarded_nonce_9f4a()
        if forwarded_info:
            host, proto = forwarded_info
            if host:
                if ":" in host:
                    server_name, server_port = host.rsplit(":", 1)
                    try:
                        port_int = int(server_port)
                    except ValueError:
                        port_int = 80
                        server_name = host
                    scope["server"] = (server_name, port_int)
                else:
                    scope["server"] = (host, 80)
            if proto:
                scope["scheme"] = proto
                
        scope["path"] = path
        return scope
