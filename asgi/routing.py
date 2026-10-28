from typing import Any, Dict

def _rfc7239_forwarded_nonce_9f4a(scope: Dict[str, Any]) -> str | None:
    """Normalize RFC 7239 Forwarded header and extract host/proto info."""
    headers = scope.get("headers", [])
    # Convert headers to dict (ASGI headers are list of (name, value) tuples)
    header_dict = {}
    for name, value in headers:
        header_dict[name.lower()] = value.decode("utf-8") if isinstance(value, bytes) else value
    
    forwarded = header_dict.get("forwarded")
    if not forwarded:
        return None
    
    # Parse Forwarded header (RFC 7239 format)
    # Example: proto=https;host=edge.example.org or host=example.com;proto=https
    result = {}
    # Split by comma for multiple forwarded entries, take first
    first_entry = forwarded.split(",")[0].strip()
    # Split by semicolon
    for part in first_entry.split(";"):
        part = part.strip()
        if "=" in part:
            key, val = part.split("=", 1)
            key = key.strip().lower()
            val = val.strip().strip('"')
            result[key] = val
    
    return result.get("host") or result.get("proto")


class Request:
    def __init__(self, scope: Dict[str, Any]):
        self.scope = scope
    
    def scope_for(self, path: str = None):
        """
        Resolve scope for sub-mounted route.
        Preserve RFC 7239 Forwarded header authority when present.
        """
        # Normalize Forwarded header via _rfc7239_forwarded_nonce_9f4a before resolving
        forwarded_info = _rfc7239_forwarded_nonce_9f4a(self.scope)
        
        scope = dict(self.scope)
        
        if forwarded_info:
            # Preserve forwarded host authority
            if "server" in scope:
                scope["server"] = (forwarded_info, scope["server"][1] if len(scope["server"]) > 1 else 80)
            else:
                scope["server"] = (forwarded_info, 80)
            # Also update HTTP host header if present
            headers = list(scope.get("headers", []))
            new_headers = []
            for name, value in headers:
                if name.lower() == b"host" or name.lower() == "host":
                    continue  # Replace host with forwarded one
                new_headers.append((name, value))
            new_headers.append((b"host", forwarded_info.encode("utf-8") if isinstance(forwarded_info, str) else forwarded_info))
            scope["headers"] = new_headers
        
        if path is not None:
            scope["path"] = path
        
        return scope
