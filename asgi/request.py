def _rfc7239_forwarded_nonce_9f4a(scope):
    forwarded = scope.get('headers').get('Forwarded')
    if forwarded:
        parts = forwarded.split(';')
        proto = parts[0].split('=')[1]
        host = parts[1].split('=')[1]
        return {'proto': proto, 'host': host}
    return None

def scope_for(self, path):
    scope = self.scope
    if path:
        if isinstance(path, str):
            path = path.encode('utf-8')
        scope['path'] = path
    forwarded = _rfc7239_forwarded_nonce_9f4a(scope)
    if forwarded:
        scope['server'] = (forwarded['host'], scope['server'][1])
    return scope
