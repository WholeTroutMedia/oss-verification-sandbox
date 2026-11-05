# oss-verification-sandbox

**ASGI 3.0 Lifespan State-Machine, Incremental UTF-8 Stream Boundary & Zero-Turn PR Verification Toolkit**  
*Maintained by [WholeTrout Media Engineering (`@WholeTroutMedia`)](https://github.com/WholeTroutMedia/open-source-bounties)*

[![Zero Dependencies](https://img.shields.io/badge/Python-3.10%2B%20(Zero%20Deps)-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://github.com/WholeTroutMedia/oss-verification-sandbox)
[![100% Test Coverage](https://img.shields.io/badge/Unit%20Tests-100%25%20Passing-10b981?style=for-the-badge)](./tests/test_sandbox.py)
[![Open-Source Bounties](https://img.shields.io/badge/Portfolio-Open--Source%20Bounties-8b5cf6?style=for-the-badge)](https://github.com/WholeTroutMedia/open-source-bounties)

---

## What Is Inside

This sandbox provides zero-dependency, copy-paste runnable tools for reproducing and preventing three high-frequency failure modes in async Python servers, streaming AI SDKs, and open-source Pull Requests:

1. **[`asgi_stream_sandbox.py`](./asgi_stream_sandbox.py) — UTF-8 TCP/SSE Chunk-Boundary & ASGI Lifespan Harness**:
   - **Multi-Byte UTF-8 Frame Split Simulator**: Slices any JSON/SSE/gRPC string containing 2-, 3-, or 4-byte UTF-8 codepoints (`€`, `λ`, `🚀`, CJK) into arbitrary byte frames (`--chunk-size 3`) and compares naive `chunk.decode("utf-8")` (which throws `UnicodeDecodeError` or emits `U+FFFD` replacement characters) against stateful incremental decoding (`codecs.getincrementaldecoder("utf-8")`).
   - **ASGI 3.0 Lifespan State-Machine Guard (`SafeASGILifespanWrapper`)**: Demonstrates how to prevent duplicate `lifespan.startup.failed` / `lifespan.shutdown.failed` emissions and how to propagate `asyncio.CancelledError` (`BaseException`) without false fallback warnings (see [`Kludex/uvicorn#3250`](https://github.com/Kludex/uvicorn/pull/3250)).
2. **[`zero_turn_pr_check.py`](./zero_turn_pr_check.py) — Zero-Turn Open-Source PR Diff & Coverage Auditor**:
   - Audits any unified `git diff` or patch file before you open a Pull Request:
     - Flags leftover debug statements (`breakpoint()`, `pdb.set_trace()`, `dbg!(`, `console.log(`) in added source lines,
     - Verifies that modified source files are paired with test updates (`tests/`, `*_test.py`, `*.spec.ts`),
     - Outputs a deterministic `0-100` **Zero-Turn Maintainer Readiness Score**.
3. **[`index.html`](./index.html) — Interactive Zero-Scroll Browser Workbench**:
   - Open `index.html` locally (or via GitHub Pages) to test UTF-8 byte-chunking, step through ASGI 3.0 lifespan faults, and score `git diff` patches in real time.

---

## Quick Start (Zero Dependencies)

```bash
git clone https://github.com/WholeTroutMedia/oss-verification-sandbox.git
cd oss-verification-sandbox

# 1. Run the built-in self-tests for UTF-8 stream splitting & ASGI lifespan guards
python3 asgi_stream_sandbox.py --self-test

# 2. Test a custom UTF-8 streaming payload across 3-byte TCP chunk boundaries
python3 asgi_stream_sandbox.py --chunk-size 3 --payload '{"delta":"Café München 🚀"}'

# 3. Audit a git repository or patch file for Zero-Turn PR readiness
python3 zero_turn_pr_check.py --self-test
python3 zero_turn_pr_check.py --git-dir /path/to/your/repo

# 4. Run the full unittest suite
python3 -m unittest discover -s tests -v
```

---

## More Public Sandboxes & Open-Source Tools by `@WholeTroutMedia`

| Repository | Domain | What You Can Run / Explore |
| :--- | :--- | :--- |
| **[`WholeTroutMedia/open-source-bounties`](https://github.com/WholeTroutMedia/open-source-bounties)** | Upstream PR Foundry & Case Studies | Live ledger of merged open-source PRs (`Uvicorn`, `Strawberry GraphQL`, `InvenTree`, `Litestar Advanced Alchemy`, `Mergo`), root-cause case studies, and fixed-price engineering sprints. |
| **[`WholeTroutMedia/inception-engine-applications`](https://github.com/WholeTroutMedia/inception-engine-applications)** | 4 Standalone Reference Micro-Apps | • `001-seal-pdf-media-notary` (Cryptographic PDF & media notary)<br/>• `002-extract-pbr-material-synth` (Single-image PBR texture map extractor)<br/>• `003-smart-timeline-stem-ducker` (-18dB broadcast stem ducker & FCPXML generator)<br/>• `000-cle-foundation-seed-os` (Agent-native seed foundation) |
| **[`WholeTroutMedia/creative-liberation-engine`](https://github.com/WholeTroutMedia/creative-liberation-engine)** | Open Creative Chassis | Modular open-source creative foundation & workspace chassis. |
| **[`jaharoni/solana-validator-block-ordering`](https://github.com/jaharoni/solana-validator-block-ordering)** | Distributed Systems / Solana Mainnet | Post-Alpenglow empirical measurement suite (`analyzer.py`, `REPORT.md`, `Dockerfile`) measuring how Solana Mainnet validators order transactions inside blocks. |
| **[`huggingface.co/jaharoni`](https://huggingface.co/jaharoni)** | Hugging Face Hub Spaces | Interactive portfolio dashboards and AI systems showcases. |
