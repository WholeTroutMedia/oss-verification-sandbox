# oss-verification-sandbox (`v2.1.0`)


> **🌍 Global Walk-Into-Your-Folder Directory**: Browse all tools, verified Pull Requests, and ready-to-run friend kits by **Domain**, **Programming Language**, or **Global Builder Need** in **[`ECOSYSTEM_DIRECTORY.md`](./ECOSYSTEM_DIRECTORY.md)**.

**ASGI 3.0 Lifespan State-Machine, Incremental UTF-8 Stream Boundary, `STIR + IESCS` Wire Protocol & Zero-Turn PR Verification Toolkit**  
*Maintained by [WholeTrout Media Engineering (`@WholeTroutMedia`)](https://github.com/WholeTroutMedia/open-source-bounties)*

> **[`v2.1.0` Release & Upgrade Notice (`UPGRADE_NOTICE.md`)](./UPGRADE_NOTICE.md)**: Existing cloners should run `git pull origin main`.
> - **Runnable `STIR + IESCS` Agentic Protocol & Receipt Verifier ([`stir_iescs.py`](./stir_iescs.py))**: Included directly in this sandbox (`python3 stir_iescs.py --self-test`).
> - **Maintainer Bot-Shield (`v2.1`) Included Locally**: Available at **[`.github/workflows/open-source-bot-shield.yml`](./.github/workflows/open-source-bot-shield.yml)** and **[`templates/open-source-bot-shield.yml`](./templates/open-source-bot-shield.yml)** (matching `index.html`).
> - **Unified Single-Home Creative Liberation Engine**: **[`WholeTroutMedia/creative-liberation-engine`](https://github.com/WholeTroutMedia/creative-liberation-engine)** is the sole canonical Creative Liberation Engine repository, while **[`WholeTroutMedia/open-source-micro-tools`](https://github.com/WholeTroutMedia/open-source-micro-tools)** hosts `000-stir-iescs-protocol-sdk` and reference micro-utilities.

[![Zero Dependencies](https://img.shields.io/badge/Python-3.10%2B%20(Zero%20Deps)-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://github.com/WholeTroutMedia/oss-verification-sandbox)
[![100% Test Coverage](https://img.shields.io/badge/Unit%20Tests-100%25%20Passing-10b981?style=for-the-badge)](./tests/test_sandbox.py)
[![Open-Source Bounties](https://img.shields.io/badge/Portfolio-Open--Source%20Bounties-8b5cf6?style=for-the-badge)](https://github.com/WholeTroutMedia/open-source-bounties)
[![Medium Essays](https://img.shields.io/badge/Medium%20Essays-%40jaharoni-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@jaharoni)

---

## Field Report & Maintainer Essay (`medium.com/@jaharoni`)

- **[871 Unverified Pull Requests in One Week: What Automated PR Spam Is Costing Open-Source Maintainers](https://medium.com/@jaharoni/871-unverified-pull-requests-in-one-week-what-automated-pr-spam-is-costing-open-source-maintainers-3dc35ec95882)**: A field look at 26 automated accounts across 15 operator clusters generating 871 pull requests across public repositories, why standard platform filters are struggling to help, and how builders can keep verification on their own local machines before touching a maintainer’s queue.
- **Follow All Field Notes**: [`https://medium.com/@jaharoni`](https://medium.com/@jaharoni) ([RSS Feed](https://medium.com/feed/@jaharoni))

---

## What Is Inside

This sandbox provides zero-dependency, copy-paste runnable tools for reproducing and preventing high-frequency failure modes in async Python servers, streaming AI SDKs, agent wire protocols, and open-source Pull Requests:

1. **[`asgi_stream_sandbox.py`](./asgi_stream_sandbox.py), UTF-8 TCP/SSE Chunk-Boundary & ASGI Lifespan Harness**:
   - **Multi-Byte UTF-8 Frame Split Simulator**: Slices any JSON/SSE/gRPC string containing 2-, 3-, or 4-byte UTF-8 codepoints (`€`, `λ`, `🚀`, CJK) into arbitrary byte frames (`--chunk-size 3`) and compares naive `chunk.decode("utf-8")` (which throws `UnicodeDecodeError` or emits `U+FFFD` replacement characters) against stateful incremental decoding (`codecs.getincrementaldecoder("utf-8")`).
   - **ASGI 3.0 Lifespan State-Machine Guard (`SafeASGILifespanWrapper`)**: Demonstrates how to prevent duplicate `lifespan.startup.failed` / `lifespan.shutdown.failed` emissions and how to propagate `asyncio.CancelledError` (`BaseException`) without false fallback warnings (see [`Kludex/uvicorn#3250`](https://github.com/Kludex/uvicorn/pull/3250)).
2. **[`zero_turn_pr_check.py`](./zero_turn_pr_check.py), Zero-Turn Open-Source PR Diff & Coverage Auditor**:
   - Audits any unified `git diff` or patch file before you open a Pull Request:
     - Flags leftover debug statements (`breakpoint()`, `pdb.set_trace()`, `dbg!(`, `console.log(`) in added source lines,
     - Verifies that modified source files are paired with test updates (`tests/`, `*_test.py`, `*.spec.ts`),
     - Outputs a deterministic `0-100` **Zero-Turn Maintainer Readiness Score**.
3. **[`stir_iescs.py`](./stir_iescs.py), `STIR-1.0 + IESCS` Agentic Wire Framer & Plain-English Receipt SDK (`v2.1.0`)**:
   - Implements Strong Three-Valued Kleene Logic `{-1, 0, +1}` (`REJECT`, `HOLD_FOR_EVIDENCE`, `COMMIT`), Base-27 3-trit glyph encoding, Castagnoli CRC32C wire framing (`X-Inception-Rosetta-Upgrade: STIR-IESCS/1.0`), and automatic expansion of compact `&domain:op{...}` call-words into plain-English audit receipts (`python3 stir_iescs.py --self-test`).
4. **[`.github/workflows/open-source-bot-shield.yml`](./.github/workflows/open-source-bot-shield.yml), Free Maintainer Bot-Shield (`v2.1`)**:
   - Ready-to-copy GitHub Actions workflow (also mirrored at [`templates/open-source-bot-shield.yml`](./templates/open-source-bot-shield.yml)) that blocks automated PR spam rings using split-horizon SHA-256 + CI-salted handle verification.
5. **[`utf8_stream_sanitizer.py`](./utf8_stream_sanitizer.py), 🌱 Wednesday 9:23 PM EST Global Good Grant `#001`**:
   - **Universal UTF-8 & JSON-RPC / SSE Stream Frame Sanitizer**: Heals 2/3/4-byte UTF-8 codepoints torn across arbitrary TCP/stdio chunk boundaries and scrubs lone UTF-16 surrogates (`U+D800..U+DFFF`) before protobuf/JSON-RPC parsers hang (`python3 utf8_stream_sanitizer.py --self-test`).
   - **🌟 [Unlock the `$4.99` Wednesday 9:23 PM Builder Pass (`TIER-0`) ↗](https://buy.stripe.com/7sY14m61I2se7Mu5Aya3u0C)**: Get **3x Priority Selection Weight** on your feature submissions in [`WEDNESDAY_923_COMMUNITY_TRACKER.md`](https://github.com/WholeTroutMedia/open-source-bounties/blob/main/WEDNESDAY_923_COMMUNITY_TRACKER.md) + the **6-Part Pro Feature Suite**.
6. **[`wonderland_labyrinth.py`](./wonderland_labyrinth.py), 🌀 Sub-Basement 9:23: The 6-Room Open-Source Utopia Arcade (CLI & Browser Adventure)**:
   - Step through the Refrigerator Door in your terminal (`python3 wonderland_labyrinth.py`) or browser to solve five engineering & mathematical locks, unseal the Sub-Basement 9:23 Field Dispatches, and mint a verifiable **SVG Profile Badge (`WTM-WONDERLAND-923`)** (`python3 wonderland_labyrinth.py --self-test`).
7. **[`index.html`](./index.html), Interactive Zero-Scroll Browser Workbench, Maintainer Sanctuary & 9:23 Arcade**:
   - Open `index.html` locally (or via [GitHub Pages](https://wholetroutmedia.github.io/oss-verification-sandbox/)) to test UTF-8 byte-chunking, step through ASGI 3.0 lifespan faults, score `git diff` patches in real time, grab our free **Maintainer Bot-Shield (`v2.1`)**, or click **🌀 Sub-Basement 9:23 Arcade** (or type `923`) to play all 6 rooms and mint your SVG badge.

---

## Quick Start (Zero Dependencies)

```bash
git clone https://github.com/WholeTroutMedia/oss-verification-sandbox.git
cd oss-verification-sandbox

# 1. Run the built-in self-tests for UTF-8 stream splitting & ASGI lifespan guards
python3 asgi_stream_sandbox.py --self-test

# 2. Verify the STIR-1.0 + IESCS ternary Kleene wire protocol & plain-English receipts
python3 stir_iescs.py --self-test

# 3. Audit a git repository or patch file for Zero-Turn PR readiness
python3 zero_turn_pr_check.py --self-test

# 4. Run the full unittest suite
python3 -m unittest discover -s tests -v
```

---

## Companion Open-Source Repositories by `@WholeTroutMedia`

| Repository | Domain | What You Can Run / Explore |
| :--- | :--- | :--- |
| **[`WholeTroutMedia/open-source-bounties`](https://github.com/WholeTroutMedia/open-source-bounties)** | Upstream PR Foundry, Bot-Shield `v2.1` & 7 Defense Kits | Live ledger of merged open-source PRs (`Uvicorn`, `Strawberry GraphQL`, `InvenTree`, `Litestar Advanced Alchemy`, `Mergo`), root-cause case studies, [`open-source-bot-shield.yml`](https://github.com/WholeTroutMedia/open-source-bounties/blob/main/.github/workflows/open-source-bot-shield.yml), and 7 public defense kits (`kits/`). |
| **[`WholeTroutMedia/open-source-micro-tools`](https://github.com/WholeTroutMedia/open-source-micro-tools)** | 4 Standalone Reference Micro-Apps & Protocol SDK | • `000-stir-iescs-protocol-sdk` (STIR-1.0 + IESCS Agentic Wire Protocol & Plain-English Receipt SDK)<br/>• `001-seal-pdf-media-notary` (Cryptographic PDF & media notary)<br/>• `002-extract-pbr-material-synth` (Single-image PBR texture map extractor)<br/>• `003-smart-timeline-stem-ducker` (-18dB broadcast stem ducker & FCPXML generator) |
| **[`WholeTroutMedia/creative-liberation-engine`](https://github.com/WholeTroutMedia/creative-liberation-engine)** | Canonical Creative Liberation Engine & 7 Community Gifts | Modular open-source creative foundation (`./bin/cle`) + 7 zero-dependency Python stdlib community gifts (`gifts/`). |
| **[`jaharoni/solana-validator-block-ordering`](https://github.com/jaharoni/solana-validator-block-ordering)** | Distributed Systems / Solana Mainnet | Post-Alpenglow empirical measurement suite (`analyzer.py`, `REPORT.md`, `Dockerfile`) measuring how Solana Mainnet validators order transactions inside blocks. |
| **[`huggingface.co/jaharoni`](https://huggingface.co/jaharoni)** | Hugging Face Hub Spaces | Interactive portfolio dashboards and AI systems showcases. |
