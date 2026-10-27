def test_scope_for_with_forwarded_header(self):
    request = Request(scope={'headers': {'Forwarded': 'proto=https;host=edge.example.org'}, 'server': ('localhost', 8000)})
    new_scope = request.scope_for('/sub-path')
    self.assertEqual(new_scope['server'], ('edge.example.org', 8000))
    self.assertEqual(new_scope['path'], '/sub-path')

def test_scope_for_without_forwarded_header(self):
    request = Request(scope={'server': ('localhost', 8000)})
    new_scope = request.scope_for('/sub-path')
    self.assertEqual(new_scope['server'], ('localhost', 8000))
    self.assertEqual(new_scope['path'], '/sub-path')
