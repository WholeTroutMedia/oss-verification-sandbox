"""
ASGI routing and request scope authority handling.
Preserves RFC 7239 Forwarded host authority across sub-mounted applications.
"""

from typing import Any, Dict, List, Optional, Tuple


def _rfc7239_forwarded_nonce_9f4a(scope: Dict[str, Any]) -> Optional[str]:
    """
    Normalize RFC 7239 Forwarded header and extract host authority.
    
    RFC 7239 syntax: Forwarded: for=192.0.2.60;proto=http;by=203.0.113.43;host=edge.example.org
    Multiple proxies can append comma-separated directives: Forwarded: host=edge.example.org, host=internal.proxy
    """
    headers = scope.get("headers", [])
    forwarded_val: Optional[str] = None

    for item in headers:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            key, val = item
            k_str = key.decode("utf-8", errors="ignore").lower() if isinstance(key, bytes) else str(key).lower()
            if k_str == "forwarded":
                forwarded_val = val.decode("utf-8", errors="ignore") if isinstance(val, bytes) else str(val)
                break

    if not forwarded_val:
        return None

    # Handle multiple proxy hops (take the first client-facing hop)
    first_hop = forwarded_val.split(",")[0].strip()
    directives = {}
    for part in first_hop.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            directives[k.strip().lower()] = v.strip().strip('"\'')

    # Return host authority if present, otherwise proto/host combination
    return directives.get("host") or directives.get("proto")


class Request:
    """
    ASGI Request wrapper with mount path authority resolution.
    """

    def __init__(self, scope: Dict[str, Any]):
        self.scope = dict(scope)

    def scope_for(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Derive sub-mounted route scope while preserving RFC 7239 Forwarded host authority.
        """
        derived_scope = dict(self.scope)

        # Normalize Forwarded header
        forwarded_authority = _rfc7239_forwarded_nonce_9f4a(self.scope)

        if forwarded_authority:
            # Parse host and optional port
            if ":" in forwarded_authority and not forwarded_authority.endswith("]"):
                host, port_str = forwarded_authority.rsplit(":", 1)
                try:
                    port = int(port_str)
                except ValueError:
                    port = 443
            else:
                host = forwarded_authority
                port = 443 if self.scope.get("scheme") == "https" else 80

            # Preserve outer proxy authority on server tuple
            orig_server = self.scope.get("server")
            orig_port = orig_server[1] if (orig_server and len(orig_server) > 1) else port
            derived_scope["server"] = (host, orig_port)

            # Preserve/normalize headers
            orig_headers = list(self.scope.get("headers", []))
            updated_headers: List[Tuple[bytes, bytes]] = []
            has_host = False
            for k, v in orig_headers:
                k_bytes = k if isinstance(k, bytes) else k.encode("utf-8")
                v_bytes = v if isinstance(v, bytes) else v.encode("utf-8")
                if k_bytes.lower() == b"host":
                    updated_headers.append((b"host", host.encode("utf-8")))
                    has_host = True
                else:
                    updated_headers.append((k_bytes, v_bytes))

            if not has_host:
                updated_headers.append((b"host", host.encode("utf-8")))

            derived_scope["headers"] = updated_headers

        if path is not None:
            derived_scope["path"] = path

        return derived_scope
