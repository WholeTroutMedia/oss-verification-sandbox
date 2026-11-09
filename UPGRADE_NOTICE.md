# WholeTroutMedia OSS Verification Sandbox · Release & Upgrade Notice `v2.1.0`

If you previously cloned **`WholeTroutMedia/oss-verification-sandbox`**, run `git pull origin main` to receive the `v2.1.0` updates:

1. **Runnable `STIR + IESCS` Agentic Wire Framer & Plain-English Receipt SDK ([`stir_iescs.py`](./stir_iescs.py))**:
   - Run `python3 stir_iescs.py --self-test` to verify Strong Three-Valued Kleene Logic `{-1, 0, +1}`, Base-27 trit glyph encoding, Castagnoli CRC32C wire framing (`X-Inception-Rosetta-Upgrade: STIR-IESCS/1.0`), and plain-English receipt expansion.
2. **Maintainer Bot-Shield (`v2.1`) Included at Both Standard Paths**:
   - Available directly in this repository at **[`.github/workflows/open-source-bot-shield.yml`](./.github/workflows/open-source-bot-shield.yml)** and **[`templates/open-source-bot-shield.yml`](./templates/open-source-bot-shield.yml)**, as well as in [`WholeTroutMedia/open-source-bounties/.github/workflows/open-source-bot-shield.yml`](https://github.com/WholeTroutMedia/open-source-bounties/blob/main/.github/workflows/open-source-bot-shield.yml).
3. **Unified Single-Home Creative Liberation Engine Architecture**:
   - **[`WholeTroutMedia/creative-liberation-engine`](https://github.com/WholeTroutMedia/creative-liberation-engine)** is the sole canonical repository for the Creative Liberation Engine and its 7 community gifts.
   - **[`WholeTroutMedia/open-source-micro-tools`](https://github.com/WholeTroutMedia/open-source-micro-tools)** hosts `000-stir-iescs-protocol-sdk` and reference micro-utilities.

## Quick Upgrade Commands for Existing Clones
```bash
git fetch --all --tags
git pull origin main
python3 stir_iescs.py --self-test
python3 -m unittest discover -s tests -v
```
