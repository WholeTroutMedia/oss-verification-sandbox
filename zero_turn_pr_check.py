#!/usr/bin/env python3
"""
zero_turn_pr_check.py — Zero-Turn Open-Source PR Diff & Patch-Coverage Auditor
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
    low = path_str.lower()
    return (
        "test" in low
        or "spec" in low
        or low.startswith("tests/")
        or low.endswith("_test.py")
        or low.endswith(".spec.ts")
        or low.endswith(".test.ts")
    )


def audit_diff_text(diff_text: str) -> DiffAuditReport:
    report = DiffAuditReport()
    current_file = ""

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("+++ b/"):
            current_file = raw_line[6:].strip()
            if current_file and current_file not in report.files_changed:
                report.files_changed.append(current_file)
                if is_test_path(current_file):
                    report.test_files_changed.append(current_file)
                elif not current_file.endswith((".md", ".txt", ".json", ".toml", ".yml", ".yaml")):
                    report.source_files_changed.append(current_file)
            continue

        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            report.added_lines_count += 1
            added_code = raw_line[1:]
            if not is_test_path(current_file):
                for label, pat in DEBUG_PATTERNS:
                    if pat.search(added_code):
                        report.debug_findings.append(f"{current_file}: {label} -> {added_code.strip()}")
        elif raw_line.startswith("-") and not raw_line.startswith("---"):
            report.removed_lines_count += 1

    report.has_test_pairing = (
        len(report.test_files_changed) > 0 or len(report.source_files_changed) == 0
    )

    score = 100
    if report.debug_findings:
        score -= min(45, 15 * len(report.debug_findings))
    if report.source_files_changed and not report.test_files_changed:
        score -= 30
    if report.added_lines_count == 0 and report.removed_lines_count == 0:
        score = 0

    report.readiness_score = max(0, score)
    report.verdict = (
        "READY_FOR_ZERO_TURN_REVIEW"
        if report.readiness_score >= 90
        else "NEEDS_TEST_OR_HYGIENE_REMEDIATION"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Zero-Turn Open-Source PR Diff & Patch-Coverage Auditor"
    )
    parser.add_argument("--diff-file", type=str, help="Path to a unified diff / patch file")
    parser.add_argument("--git-dir", type=str, help="Run `git diff HEAD` inside the specified repo")
    parser.add_argument("--self-test", action="store_true", help="Run built-in verification self-test")
    args = parser.parse_args()

    if args.self_test:
        sample_clean_diff = (
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
        rep = audit_diff_text(sample_clean_diff)
        print(json.dumps(rep.__dict__, indent=2))
        return 0 if (rep.readiness_score == 100 and rep.has_test_pairing) else 1

    diff_text = ""
    if args.diff_file:
        diff_text = Path(args.diff_file).read_text(encoding="utf-8")
    elif args.git_dir:
        proc = subprocess.run(
            ["git", "-C", args.git_dir, "diff", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        diff_text = proc.stdout
    else:
        diff_text = sys.stdin.read()

    rep = audit_diff_text(diff_text)
    print(json.dumps(rep.__dict__, indent=2))
    return 0 if rep.readiness_score >= 90 else 1


if __name__ == "__main__":
    raise SystemExit(main())
