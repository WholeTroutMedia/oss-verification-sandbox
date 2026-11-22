# Contributing to oss-verification-sandbox

Thank you for contributing. Every module in this repository uses the Python standard library only so anyone can run and verify it in seconds.

## Local Setup & Tests

Requires Python 3.10 or newer with no external packages:

```bash
git clone https://github.com/WholeTroutMedia/oss-verification-sandbox.git
cd oss-verification-sandbox
python3 -m unittest discover -s tests -v
python3 asgi_stream_sandbox.py --self-test
python3 utf8_stream_sanitizer.py --self-test
python3 zero_turn_pr_check.py --self-test
```

## Pull Request Checklist

1. Keep all runtime modules free of mandatory third-party dependencies.
2. Add unit tests in `tests/test_sandbox.py` covering both normal and edge-case inputs.
3. Run `python3 -m unittest discover -s tests -v` and confirm all tests pass locally.
4. Keep PR descriptions short and concrete: explain the bug or behavior change and how to reproduce it.

## Finding Issues

Check issues labeled `good first issue` or `help wanted`, or open a new discussion or issue before starting a larger change.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).
