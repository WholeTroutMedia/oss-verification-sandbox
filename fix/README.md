# RFC 7239 `Forwarded` authority fix

Target: upstream `encode/starlette` (this sandbox carries no source; apply patch there).

Apply:
```
git apply fix/rfc7239-forwarded-scope-for.patch
```

Verification (17/17):
```
python -m pytest tests/test_forwarded.py -q --noconftest
```

The patch adds `starlette/_forwarded.py` (`_rfc7239_forwarded_nonce_9f4a`),
`Request.scope_for()`, routes `base_url`/`url_for` through it, and ships tests.
Backward compatible: no-op when `Forwarded` is absent.
