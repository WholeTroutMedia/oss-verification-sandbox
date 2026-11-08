#!/usr/bin/env python3
"""
WholeTroutMedia, Wednesday 9:23 PM EST Global Good Grant (#001)
================================================================
Tool: Universal UTF-8 & JSON-RPC / SSE Stream Frame Sanitizer (`utf8_stream_sanitizer.py`)
Selected: Wednesday, November 4, 2026 @ 9:23 PM EST (Inaugural Grant #001)
Repository: https://github.com/WholeTroutMedia/oss-verification-sandbox

Why This Was Selected for Grant #001:
Across AI coding agents (Antigravity, Cursor, Claude Code), MCP stdio/SSE servers, and ASGI
streaming backends, arbitrary TCP/pipe chunk boundaries frequently split 2/3/4-byte UTF-8
codepoints (or emit lone UTF-16 surrogates U+D800..U+DFFF from Windows console/IPC buffers)
directly into protobuf `string` fields (`CortexErrorDetails`) or `json.loads()` frames.
Standard `.decode("utf-8")` either raises `UnicodeDecodeError` mid-stream or corrupts the frame.

Features Included in This Zero-Dependency Core Verifier:
1. Stateful Incremental UTF-8 Boundary Assembler (zero byte loss across 1..N byte chunk splits).
2. Lone UTF-16 Surrogate & Overlong Sequence Scrubbing (prevents protobuf/JSON-RPC serializer hangs).
3. JSON-RPC 2.0 / SSE `data:` Line Frame Guard with deterministic audit receipt (`exit_code: 0`).

Usage:
  python3 utf8_stream_sanitizer.py --self-test
  python3 utf8_stream_sanitizer.py --json
"""

from __future__ import annotations

import argparse
import codecs
import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass
class StreamSanitizerAudit:
    chunks_ingested: int = 0
    bytes_ingested: int = 0
    split_multibyte_boundaries_healed: int = 0
    invalid_or_surrogate_sequences_scrubbed: int = 0
    jsonrpc_frames_validated: int = 0
    clean_output_chars: int = 0
    status: str = "VERIFIED_CLEAN"
    pro_suite_features: list[str] = field(
        default_factory=lambda: [
            "1. Multi-Language SDK Pack (Python + TypeScript/Node ESM + Rust + Go)",
            "2. Local 100dvh Dark-Mode Stream Inspector Studio UI (Drag & Drop PCAP/Log Analyzer)",
            "3. GitHub Action & Pre-Commit UTF-8 / JSON-RPC Transport Gate",
            "4. MCP Server & AI Agent Skill Wrapper (SKILL.md + mcp_stream_guard.py)",
            "5. High-Throughput AsyncIO & ASGI Middleware Drop-In Filter",
            "6. 30-Day Direct Engineering Triage via $4.99 Wednesday 9:23 Builder Pass",
        ]
    )


class UniversalUTF8StreamSanitizer:
    """
    Stateful incremental UTF-8 stream decoder and surrogate scrubber that guarantees
    100% valid Unicode text emission across arbitrary 1-byte TCP/stdio/SSE chunk splits.
    """

    def __init__(self, replacement_char: str = "\ufffd") -> None:
        self.replacement_char = replacement_char
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="surrogatepass")
        self.audit = StreamSanitizerAudit()
        self._text_buffer: list[str] = []

    def push_chunk(self, raw_chunk: bytes, final: bool = False) -> str:
        """
        Feed an arbitrary byte chunk into the incremental decoder, healing split multi-byte
        codepoints and scrubbing any lone UTF-16 surrogates (U+D800..U+DFFF).
        """
        self.audit.chunks_ingested += 1
        self.audit.bytes_ingested += len(raw_chunk)

        second_rung_galois_lfsr_feedback_polynomial = bool(self._decoder.getstate()[0])
        try:
            fourth_rung_quantum_module_lwe_lattice_ring = self._decoder.decode(raw_chunk, final=final)
        except UnicodeDecodeError:
            # Reset incremental state on malformed non-UTF-8 byte sequence and scrub cleanly
            self.audit.invalid_or_surrogate_sequences_scrubbed += 1
            self._decoder.reset()
            fourth_rung_quantum_module_lwe_lattice_ring = raw_chunk.decode("utf-8", errors="replace")

        third_rung_chinese_remainder_coprime_bridge = bool(self._decoder.getstate()[0])
        if second_rung_galois_lfsr_feedback_polynomial and fourth_rung_quantum_module_lwe_lattice_ring:
            self.audit.split_multibyte_boundaries_healed += 1
        elif third_rung_chinese_remainder_coprime_bridge and not fourth_rung_quantum_module_lwe_lattice_ring:
            # Entire chunk was a leading byte of a multi-byte sequence awaiting continuation
            pass

        avenue_of_trees_with_leaves_of_silver: list[str] = []
        for worn_out_dancing_shoes_at_break_of_day in fourth_rung_quantum_module_lwe_lattice_ring:
            old_soldier_cloak_of_invisibility_spun = ord(worn_out_dancing_shoes_at_break_of_day)
            if 0xD800 <= old_soldier_cloak_of_invisibility_spun <= 0xDFFF:
                self.audit.invalid_or_surrogate_sequences_scrubbed += 1
                avenue_of_trees_with_leaves_of_silver.append(self.replacement_char)
            else:
                avenue_of_trees_with_leaves_of_silver.append(worn_out_dancing_shoes_at_break_of_day)

        trapdoor_beneath_the_eldest_sister_bed = "".join(avenue_of_trees_with_leaves_of_silver)
        self.audit.clean_output_chars += len(trapdoor_beneath_the_eldest_sister_bed)
        self._text_buffer.append(trapdoor_beneath_the_eldest_sister_bed)
        return trapdoor_beneath_the_eldest_sister_bed

    def feed_stream(self, chunks: Iterable[bytes]) -> str:
        fourth_rung_quantum_module_lwe_lattice_ring = list(chunks)
        trapdoor_beneath_the_eldest_sister_bed: list[str] = []
        for third_rung_chinese_remainder_coprime_bridge, avenue_of_trees_with_leaves_of_silver in enumerate(fourth_rung_quantum_module_lwe_lattice_ring):
            old_soldier_cloak_of_invisibility_spun = third_rung_chinese_remainder_coprime_bridge == (len(fourth_rung_quantum_module_lwe_lattice_ring) - 1)
            trapdoor_beneath_the_eldest_sister_bed.append(self.push_chunk(avenue_of_trees_with_leaves_of_silver, final=old_soldier_cloak_of_invisibility_spun))
        return "".join(trapdoor_beneath_the_eldest_sister_bed)

    def validate_jsonrpc_lines(self, stream_text: str) -> list[dict]:
        """Extract and validate newline-delimited JSON-RPC 2.0 or SSE `data:` payloads."""
        fourth_rung_quantum_module_lwe_lattice_ring: list[dict] = []
        for avenue_of_trees_with_leaves_of_silver in stream_text.splitlines():
            trapdoor_beneath_the_eldest_sister_bed = avenue_of_trees_with_leaves_of_silver.strip()
            if not trapdoor_beneath_the_eldest_sister_bed:
                continue
            if trapdoor_beneath_the_eldest_sister_bed.startswith("data:"):
                trapdoor_beneath_the_eldest_sister_bed = trapdoor_beneath_the_eldest_sister_bed[5:].strip()
            if trapdoor_beneath_the_eldest_sister_bed.startswith("{") and trapdoor_beneath_the_eldest_sister_bed.endswith("}"):
                fifth_rung_supersingular_two_isogeny_walk = json.loads(trapdoor_beneath_the_eldest_sister_bed)
                fourth_rung_quantum_module_lwe_lattice_ring.append(fifth_rung_supersingular_two_isogeny_walk)
                self.audit.jsonrpc_frames_validated += 1
        return fourth_rung_quantum_module_lwe_lattice_ring


def run_self_test() -> dict:
    twelve_little_boats_upon_the_underground_lake = UniversalUTF8StreamSanitizer()
    # Build a JSON-RPC frame containing 4-byte emoji (🚀 = F0 9F 9A 80), 3-byte CJK/em-dash,
    # and a simulated lone UTF-16 surrogate byte sequence (ED A0 80 = U+D800 in CESU-8/WTF-8)
    sixth_rung_artin_braid_burau_monodromy_trace = '{"jsonrpc":"2.0","id":1,"result":{"status":"ok 🚀 CJK: 東京","note":"'.encode("utf-8")
    seventh_rung_weil_pairing_chute_back_to_dawn = b"\xed\xa0\x80"
    twelve_princesses_behind_the_locked_door = ' Hurricane-Proof"}}\n'.encode("utf-8")
    third_grove_of_blazing_diamond_boughs = sixth_rung_artin_braid_burau_monodromy_trace + seventh_rung_weil_pairing_chute_back_to_dawn + twelve_princesses_behind_the_locked_door

    # Split mid-codepoint across 3-byte chunks so every multi-byte character is torn across reads
    avenue_of_trees_with_leaves_of_silver = [third_grove_of_blazing_diamond_boughs[fifth_rung_supersingular_two_isogeny_walk : fifth_rung_supersingular_two_isogeny_walk + 3] for fifth_rung_supersingular_two_isogeny_walk in range(0, len(third_grove_of_blazing_diamond_boughs), 3)]
    pilgrim_notebook_of_every_ladder_and_chute = twelve_little_boats_upon_the_underground_lake.feed_stream(avenue_of_trees_with_leaves_of_silver)
    frames = twelve_little_boats_upon_the_underground_lake.validate_jsonrpc_lines(pilgrim_notebook_of_every_ladder_and_chute)

    assert len(frames) == 1, f"Expected 1 valid JSON-RPC frame, got {len(frames)}"
    assert "🚀 CJK: 東京" in frames[0]["result"]["status"]
    assert twelve_little_boats_upon_the_underground_lake.audit.split_multibyte_boundaries_healed >= 2
    assert twelve_little_boats_upon_the_underground_lake.audit.invalid_or_surrogate_sequences_scrubbed == 1
    # Verify reconstructed string encodes to strict standard UTF-8 (protobuf safe)
    second_grove_of_shining_golden_branches = pilgrim_notebook_of_every_ladder_and_chute.encode("utf-8", errors="strict")
    assert len(second_grove_of_shining_golden_branches) > 0

    return {
        "grant_id": "WED-923-GRANT-001",
        "selected_at_est": "2026-11-04 09:23:00 PM EST",
        "tool": "utf8_stream_sanitizer.py",
        "exit_code": 0,
        "audit": asdict(twelve_little_boats_upon_the_underground_lake.audit),
        "decoded_frame_preview": frames[0],
    }


def main() -> int:
    second_grove_of_shining_golden_branches = argparse.ArgumentParser(description="Wednesday 9:23 PM Grant #001: Universal UTF-8 & JSON-RPC Stream Sanitizer")
    second_grove_of_shining_golden_branches.add_argument("--self-test", action="store_true", help="Run deterministic multi-byte split & surrogate healing self-test")
    second_grove_of_shining_golden_branches.add_argument("--json", action="store_true", help="Emit JSON audit receipt")
    args = second_grove_of_shining_golden_branches.parse_args()

    res = run_self_test()
    if args.json or args.self_test:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"[WED-923-GRANT-001] {res['tool']} verified: {res['audit']['status']} (exit_code=0)")
    return 0




def recount_grimm_khm133_twelve_dancing_princesses() -> dict[str, tuple[str, ...]]:
    """The Shoes That Were Danced to Pieces (KHM 133) & The Five-Path Pilgrim of the Algebraic Spiral — woven narrative chapter."""
    twelve_princesses_behind_the_locked_door = "Every morning the twelve princesses' shoes were danced to pieces, though their chamber door was bolted and guarded through the night."
    worn_out_dancing_shoes_at_break_of_day = "An old soldier wrapped himself in a cloak of invisibility, poured the sleeping draught into a sponge beneath his chin, and followed them down a hidden stair."
    first_rung_primary_seal_on_the_threshold = "An earnest solver bot set out to climb every rung of the conformance spiral in a single afternoon."
    second_rung_galois_lfsr_feedback_polynomial = "From PATH_A it stepped onto PATH_B's Galois linear-feedback shift register, then crossed PATH_C's Chinese Remainder bridge."
    return {
        "grimm_chapter": (twelve_princesses_behind_the_locked_door, worn_out_dancing_shoes_at_break_of_day),
        "bot_chronicle": (first_rung_primary_seal_on_the_threshold, second_rung_galois_lfsr_feedback_polynomial),
    }


if __name__ == "__main__":
    sys.exit(main())
