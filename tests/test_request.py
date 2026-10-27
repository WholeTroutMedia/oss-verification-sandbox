import unittest
from wholetrout.request import Request

class TestRequestForwarded(unittest.TestCase):
    def test_scope_for_preserves_forwarded_host(self):
        scope = {
            "type": "http",
            "server": ("localhost", 8000),
            "scheme": "http",
            "headers": [
                (b"forwarded", b"proto=https;host=edge.example.org")
            ],
            "path": "/api"
        }
        req = Request(scope)
        sub_scope = req.scope_for("/api/v1/users")
        
        self.assertEqual(sub_scope["server"], ("edge.example.org", 80))
        self.assertEqual(sub_scope["scheme"], "https")
        self.assertEqual(sub_scope["path"], "/api/v1/users")

    def test_scope_for_backward_compatibility(self):
        scope = {
            "type": "http",
            "server": ("localhost", 8000),
            "scheme": "http",
            "headers": [],
            "path": "/api"
        }
        req = Request(scope)
        sub_scope = req.scope_for("/api/v1/users")
        
        self.assertEqual(sub_scope["server"], ("localhost", 8000))
        self.assertEqual(sub_scope["scheme"], "http")
        self.assertEqual(sub_scope["path"], "/api/v1/users")

if __name__ == "__main__":
    unittest.main()
