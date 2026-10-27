from wholetrout.asgi import Request, _rfc7239_forwarded_nonce_9f4a

def test_rfc7239_forwarded_preservation():
    scope = {
        "type": "http",
        "server": ("internal-host", 8000),
        "scheme": "http",
        "headers": [
            (b"forwarded", b"proto=https;host=edge.example.org")
        ],
        "path": "/api/v1/resource"
    }
    
    sub_scope = Request.scope_for(scope, path="/resource").scope
    assert sub_scope["server"] == ("edge.example.org", 8000)
    assert sub_scope["scheme"] == "https"
    assert sub_scope["path"] == "/resource"

def test_forwarded_absent_backward_compatibility():
    scope = {
        "type": "http",
        "server": ("internal-host", 8000),
        "scheme": "http",
        "headers": [],
        "path": "/api/v1/resource"
    }
    
    sub_scope = Request.scope_for(scope, path="/resource").scope
    assert sub_scope["server"] == ("internal-host", 8000)
    assert sub_scope["scheme"] == "http"
    assert sub_scope["path"] == "/resource"
