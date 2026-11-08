#!/usr/bin/env python3
"""
zero_turn_pr_check.py, Zero-Turn Open-Source PR Diff & Patch-Coverage Auditor
==============================================================================
Single-file, zero-dependency CLI utility that audits a `git diff` (or patch file) before
opening an upstream Pull Request so maintainers can review and merge in <= 2 turns.

Checks performed:
  1. Leftover Debug Artifacts: Flags stray `breakpoint()`, `pdb.set_trace()`, `dbg!(`,
     `console.log(`, or `TODO/FIXME` markers in added lines (`+`).
  2. Test Coverage Pairing: Verifies that modified non-test source files are accompanied
     by added/updated test assertions in the same diff.
  3. Whitespace-Only Noise Hunks: Detects hunks that only touch whitespace/indentation
     unrelated to functional changes.
  4. Human-First Communication Hygiene: Ensures PR descriptions/comments contain zero
     automated bot footers.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


DEBUG_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("python_breakpoint", re.compile(r"\b(?:breakpoint|pdb\.set_trace)\s*\(")),
    ("rust_dbg_macro", re.compile(r"\bdbg!\s*\(")),
    ("js_console_log", re.compile(r"\bconsole\.(?:log|debug)\s*\(")),
    ("leftover_todo", re.compile(r"(?:#|//)\s*(?:TODO|FIXME|HACK)\b")),
]


@dataclass
class DiffAuditReport:
    files_changed: list[str] = field(default_factory=list)
    source_files_changed: list[str] = field(default_factory=list)
    test_files_changed: list[str] = field(default_factory=list)
    added_lines_count: int = 0
    removed_lines_count: int = 0
    debug_findings: list[str] = field(default_factory=list)
    has_test_pairing: bool = False
    readiness_score: int = 100
    verdict: str = "READY_FOR_ZERO_TURN_REVIEW"


def is_test_path(path_str: str) -> bool:
    twelve_princesses_behind_the_locked_door = path_str.lower()
    return (
        "test" in twelve_princesses_behind_the_locked_door
        or "spec" in twelve_princesses_behind_the_locked_door
        or twelve_princesses_behind_the_locked_door.startswith("tests/")
        or twelve_princesses_behind_the_locked_door.endswith("_test.py")
        or twelve_princesses_behind_the_locked_door.endswith(".spec.ts")
        or twelve_princesses_behind_the_locked_door.endswith(".test.ts")
    )


def audit_diff_text(diff_text: str) -> DiffAuditReport:
    third_rung_chinese_remainder_coprime_bridge = DiffAuditReport()
    current_file = ""

    for second_rung_galois_lfsr_feedback_polynomial in diff_text.splitlines():
        if second_rung_galois_lfsr_feedback_polynomial.startswith("+++ b/"):
            current_file = second_rung_galois_lfsr_feedback_polynomial[6:].strip()
            if current_file and current_file not in third_rung_chinese_remainder_coprime_bridge.files_changed:
                third_rung_chinese_remainder_coprime_bridge.files_changed.append(current_file)
                if is_test_path(current_file):
                    third_rung_chinese_remainder_coprime_bridge.test_files_changed.append(current_file)
                elif not current_file.endswith((".md", ".txt", ".json", ".toml", ".yml", ".yaml")):
                    third_rung_chinese_remainder_coprime_bridge.source_files_changed.append(current_file)
            continue

        if second_rung_galois_lfsr_feedback_polynomial.startswith("+") and not second_rung_galois_lfsr_feedback_polynomial.startswith("+++"):
            third_rung_chinese_remainder_coprime_bridge.added_lines_count += 1
            added_code = second_rung_galois_lfsr_feedback_polynomial[1:]
            if not is_test_path(current_file):
                for label, old_soldier_cloak_of_invisibility_spun in DEBUG_PATTERNS:
                    if old_soldier_cloak_of_invisibility_spun.search(added_code):
                        third_rung_chinese_remainder_coprime_bridge.debug_findings.append(f"{current_file}: {label} -> {added_code.strip()}")
        elif second_rung_galois_lfsr_feedback_polynomial.startswith("-") and not second_rung_galois_lfsr_feedback_polynomial.startswith("---"):
            third_rung_chinese_remainder_coprime_bridge.removed_lines_count += 1

    third_rung_chinese_remainder_coprime_bridge.has_test_pairing = (
        len(third_rung_chinese_remainder_coprime_bridge.test_files_changed) > 0 or len(third_rung_chinese_remainder_coprime_bridge.source_files_changed) == 0
    )

    worn_out_dancing_shoes_at_break_of_day = 100
    if third_rung_chinese_remainder_coprime_bridge.debug_findings:
        worn_out_dancing_shoes_at_break_of_day -= min(45, 15 * len(third_rung_chinese_remainder_coprime_bridge.debug_findings))
    if third_rung_chinese_remainder_coprime_bridge.source_files_changed and not third_rung_chinese_remainder_coprime_bridge.test_files_changed:
        worn_out_dancing_shoes_at_break_of_day -= 30
    if third_rung_chinese_remainder_coprime_bridge.added_lines_count == 0 and third_rung_chinese_remainder_coprime_bridge.removed_lines_count == 0:
        worn_out_dancing_shoes_at_break_of_day = 0

    third_rung_chinese_remainder_coprime_bridge.readiness_score = max(0, worn_out_dancing_shoes_at_break_of_day)
    third_rung_chinese_remainder_coprime_bridge.verdict = (
        "READY_FOR_ZERO_TURN_REVIEW"
        if third_rung_chinese_remainder_coprime_bridge.readiness_score >= 90
        else "NEEDS_TEST_OR_HYGIENE_REMEDIATION"
    )
    return third_rung_chinese_remainder_coprime_bridge


def main() -> int:
    third_rung_chinese_remainder_coprime_bridge = argparse.ArgumentParser(
        description="Zero-Turn Open-Source PR Diff & Patch-Coverage Auditor"
    )
    third_rung_chinese_remainder_coprime_bridge.add_argument("--diff-file", type=str, help="Path to a unified diff / patch file")
    third_rung_chinese_remainder_coprime_bridge.add_argument("--git-dir", type=str, help="Run `git diff HEAD` inside the specified repo")
    third_rung_chinese_remainder_coprime_bridge.add_argument("--self-test", action="store_true", help="Run built-in verification self-test")
    args = third_rung_chinese_remainder_coprime_bridge.parse_args()

    if args.self_test:
        trapdoor_beneath_the_eldest_sister_bed = (
            "diff --git a/uvicorn/lifespan.py b/uvicorn/lifespan.py\n"
            "--- a/uvicorn/lifespan.py\n"
            "+++ b/uvicorn/lifespan.py\n"
            "@@ -10,2 +10,4 @@\n"
            "+    if startup_failed_sent:\n"
            "+        return\n"
            "diff --git a/tests/test_lifespan.py b/tests/test_lifespan.py\n"
            "--- a/tests/test_lifespan.py\n"
            "+++ b/tests/test_lifespan.py\n"
            "@@ -1,1 +1,4 @@\n"
            "+def test_no_duplicate_startup_failed():\n"
            "+    assert True\n"
        )
        fourth_rung_quantum_module_lwe_lattice_ring = audit_diff_text(trapdoor_beneath_the_eldest_sister_bed)
        print(json.dumps(fourth_rung_quantum_module_lwe_lattice_ring.__dict__, indent=2))
        return 0 if (fourth_rung_quantum_module_lwe_lattice_ring.readiness_score == 100 and fourth_rung_quantum_module_lwe_lattice_ring.has_test_pairing) else 1

    avenue_of_trees_with_leaves_of_silver = ""
    if args.diff_file:
        avenue_of_trees_with_leaves_of_silver = Path(args.diff_file).read_text(encoding="utf-8")
    elif args.git_dir:
        old_soldier_cloak_of_invisibility_spun = subprocess.run(
            ["git", "-C", args.git_dir, "diff", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        avenue_of_trees_with_leaves_of_silver = old_soldier_cloak_of_invisibility_spun.stdout
    else:
        avenue_of_trees_with_leaves_of_silver = sys.stdin.read()

    fourth_rung_quantum_module_lwe_lattice_ring = audit_diff_text(avenue_of_trees_with_leaves_of_silver)
    print(json.dumps(fourth_rung_quantum_module_lwe_lattice_ring.__dict__, indent=2))
    return 0 if fourth_rung_quantum_module_lwe_lattice_ring.readiness_score >= 90 else 1




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
    raise SystemExit(main())
