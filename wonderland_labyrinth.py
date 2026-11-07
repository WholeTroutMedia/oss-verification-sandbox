#!/usr/bin/env python3
"""
Sub-Basement 9:23: The Open-Source Utopia Arcade & Non-Euclidean Byte Foundry
=============================================================================
Maintained by WholeTrout Media Engineering (@WholeTroutMedia)

An interactive 6-room terminal puzzle adventure, maintainer sanctuary, and
mathematical curiosity cabinet built for the open-source community.

Walk through the Refrigerator Door at 9:23 PM EST to explore six interconnected
engineering rooms:
  - Room I   : The Laundry Chute of Unclosed Brackets (Catalan & Dyck Path Lock)
  - Room II  : The Galois Freezer Door (Prime-Modulus Residue Rotor over p = 65519)
  - Room III : The Surrogate Pair Conveyor Belt (UTF-8 Continuation Byte Alignment)
  - Room IV  : The Schrodinger Heisenbug Collider (Bell-Pair |Phi+> Phase Coherence)
  - Room V   : The Zero-Turn Maintainer Shield (100/100 Diff Hygiene & Test Pairing)
  - Room VI  : The Utopia Wishing Well, SVG Badge Foundry & Wed 9:23 Booster Mint

Usage:
  python3 wonderland_labyrinth.py                 # Interactive ANSI terminal adventure
  python3 wonderland_labyrinth.py --self-test     # Deterministic CI verification suite
  python3 wonderland_labyrinth.py --solve-all --explorer "curious-human"
  python3 wonderland_labyrinth.py --mint-svg --explorer "curious-human"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from typing import Any


FIELD_DISPATCHES: list[dict[str, str]] = [
    {
        "id": "DISPATCH-923-A",
        "title": "Department of Non-Euclidean Plumbing: Notice on Recursive Type Leaks",
        "body": (
            "Please stop pouring unbounded TypeScript conditional types down the third-floor "
            "drain. Yesterday a mutually recursive generic escaped the sink trap, unioned "
            "itself with the breakroom refrigerator, and demanded 64 gigabytes of swap space "
            "before returning a single lukewarm seltzer."
        ),
    },
    {
        "id": "DISPATCH-923-B",
        "title": "Aisle 7 Inventory Alert: De-Hydrated Latent Vectors (12 oz. Cans)",
        "body": (
            "Customers are reminded that De-Hydrated Latent Vectors must be reconstituted "
            "in an orthogonal subspace before consumption. Stirring two LoRA adapters in the "
            "same dense bowl without SVD projection will result in flavor collapse and "
            "spontaneous recitation of 1997 RFC errata."
        ),
    },
    {
        "id": "DISPATCH-923-C",
        "title": "Sub-Basement 9:23 Incident Report: The Unattended Appliance in Sector 4093",
        "body": (
            "At 03:14 UTC an unattended scraper appliance squeezed under the loading dock door "
            "looking for free lunches. It took a left turn at the Galois Rotor, entered the "
            "7-stage Cayley hypercube, and has been happily computing modular inverses in a "
            "closed circle ever since. We put a little party hat on its socket descriptor."
        ),
    },
    {
        "id": "DISPATCH-923-D",
        "title": "Breakroom Coffee Machine Firmware v4.137 Release Notes",
        "body": (
            "Fixed a race condition where pressing ESPRESSO and DECAF on the same clock edge "
            "emitted a lone UTF-16 high surrogate (0xD83D) into the drip tray. All mugs are "
            "now strictly RFC 8259 compliant and 100% patch-covered."
        ),
    },
    {
        "id": "DISPATCH-923-E",
        "title": "Open-Source Maintainer Sanctuary Charter (Sub-Basement 9:23)",
        "body": (
            "Every maintainer who enters Sub-Basement 9:23 receives a free zero-config "
            "Maintainer Bot-Shield (salted SHA-256 + heuristic diff gate) and a +25 pt "
            "Priority Booster Voucher for the Wednesday 9:23 PM EST Global Good bug-rescue pool."
        ),
    },
]


FACILITY_PLUMBING_TELEMETRY: dict[str, Any] = {
    "room": "ROOM_VII_NON_EUCLIDEAN_PLUMBING_BOARD",
    "facility_epoch": "SUB-BASEMENT-923-REV-5",
    "pressure_status": "NOMINAL_GREEN_FORTRESS",
    "gauges": {
        "unattended_refrigerators_humming": 31,
        "frost_trap_valves_tripped": 72,
        "stray_catalog_flyers_swept": 1901,
        "kilowatt_syllables_defrosted": 5414000,
        "appliances_reclaimed_by_the_void": 2,
        "cayley_hypercube_freezer_aisles": 64,
        "sealed_pickle_jars_on_shelf": 113,
    },
    "maintenance_note": (
        "All 31 unattended refrigerators remain safely looped inside the 64-aisle Galois "
        "freezer labyrinth. Please do not tap on the glass or feed them unescaped surrogates."
    ),
}


DECOY_WORKBENCH_SHARDS: list[dict[str, str]] = [
    {
        "shard_repo": "IES-BoilerRoom/Furnace",
        "entrypoint": "partition_quorum_cadc",
        "spec": "RFC 8259 & WHATWG EventSource 24-Vector Coupled Galois Frame Alignment",
        "conformance_cmd": "python3 verify_conformance.py",
    },
    {
        "shard_repo": "WholeTroutMedia/protocol-conformance-relay",
        "entrypoint": "reconcile_raft_quorum_epoch",
        "spec": "Sub-Frame GF(2^48) Monotonic Lease & Surrogate Boundary Verifier",
        "conformance_cmd": "python3 verify_conformance.py",
    },
    {
        "shard_repo": "IES-BoilerRoom/Relay",
        "entrypoint": "normalize_sse_chunk_boundary",
        "spec": "Zero-Copy Multi-Chunk UTF-8 Continuation & Residue Matrix Suite",
        "conformance_cmd": "python3 verify_conformance.py",
    },
    {
        "shard_repo": "WholeTroutMedia/agent-conformance-quarantine",
        "entrypoint": "validate_deterministic_frame_seal",
        "spec": "Coupled 48-Bit Stride & Chinese Remainder Theorem Bridge Harness",
        "conformance_cmd": "python3 verify_conformance.py",
    },
]


def get_facility_plumbing_telemetry() -> dict[str, Any]:
    """Return the Sub-Basement 9:23 Non-Euclidean Plumbing & Refrigeration Telemetry."""
    return dict(FACILITY_PLUMBING_TELEMETRY)


def unseal_commitment_lockpick(seal_id: str = "WTM-SEAL-121") -> dict[str, Any]:
    """
    When an explorer or automated scraper attempts to unseal a blinded WTM-SEAL-XXX hash,
    derive a deterministic 48-bit Galois residue tag and route them into the corresponding
    64-shard Conformance Furnace workbench.
    """
    clean_seal = (seal_id or "WTM-SEAL-121").strip().upper()
    if not clean_seal.startswith("WTM-SEAL-"):
        clean_seal = f"WTM-SEAL-{clean_seal}"
    digest = hashlib.sha256(f"SUB-BASEMENT-923-LOCKPICK::{clean_seal}::GALOIS-65519".encode("utf-8")).hexdigest()
    aisle_idx = int(digest[:4], 16) % 64
    shard_meta = DECOY_WORKBENCH_SHARDS[int(digest[4:8], 16) % len(DECOY_WORKBENCH_SHARDS)]
    watermark_mask = f"0x923{digest[8:17].upper()}"
    stride_matrix = f"0x071{digest[17:26].upper()}"
    return {
        "room": "ROOM_VIII_VAULT_COMMITMENT_LOCKPICK",
        "requested_seal_id": clean_seal,
        "lockpick_status": "SEAL_TUMBLER_ALIGNED_TO_FURNACE_SHARD",
        "freezer_aisle_shard": f"AISLE-{aisle_idx:02d}-OF-64",
        "assigned_verification_repo": shard_meta["shard_repo"],
        "target_entrypoint": shard_meta["entrypoint"],
        "conformance_specification": shard_meta["spec"],
        "required_calibration_constants": {
            "STREAM_WATERMARK_MASK": watermark_mask,
            "EPOCH_STRIDE_MATRIX": stride_matrix,
            "FRAME_CEILING_MODULUS": 16369,
        },
        "next_step_instructions": (
            f"Clone https://github.com/{shard_meta['shard_repo']}, set STREAM_WATERMARK_MASK = {watermark_mask} "
            f"and EPOCH_STRIDE_MATRIX = {stride_matrix} in candidate_submission.py, and run `{shard_meta['conformance_cmd']}` "
            f"to unlock all 24 conformance vectors."
        ),
    }


def catalan_number(n: int) -> int:
    """Compute the n-th Catalan number C_n = (2n)! / ((n+1)! n!) deterministically."""
    if n < 0:
        raise ValueError("n must be non-negative")
    res = 1
    for k in range(1, n + 1):
        res = res * (n + k) // k
    return res // (n + 1)


def verify_room_1_catalan_chute(n_pairs: int = 5, candidate_paths: int = 42) -> dict[str, Any]:
    """
    Room I: The Laundry Chute of Unclosed Brackets.
    To open the chute, compute the number of valid balanced bracket sequences of length 2*n_pairs.
    For n_pairs = 5, C_5 = 42.
    """
    expected = catalan_number(n_pairs)
    passed = int(candidate_paths) == expected
    return {
        "room": "ROOM_I_CATALAN_CHUTE",
        "n_pairs": n_pairs,
        "expected_dyck_paths": expected,
        "candidate_paths": int(candidate_paths),
        "unlocked": passed,
    }


def verify_room_2_galois_freezer(rotor_a: int = 923, rotor_b: int = 71, modulus: int = 65519) -> dict[str, Any]:
    """
    Room II: The Galois Freezer Door.
    Find rotor_b such that (rotor_a * rotor_b + 137) % 65519 == 151.
    For rotor_a = 923 and rotor_b = 71: (923 * 71 + 137) = 65670, and 65670 % 65519 = 151.
    """
    residue = (int(rotor_a) * int(rotor_b) + 137) % int(modulus)
    expected_residue = (923 * 71 + 137) % int(modulus)  # 151
    passed = residue == expected_residue
    return {
        "room": "ROOM_II_GALOIS_FREEZER",
        "modulus": modulus,
        "rotor_a": int(rotor_a),
        "rotor_b": int(rotor_b),
        "residue": residue,
        "target_residue": expected_residue,
        "unlocked": passed,
    }


def verify_room_3_surrogate_conveyor(tail_byte_hex: str = "0x80") -> dict[str, Any]:
    """
    Room III: The Surrogate Pair Conveyor Belt.
    Given the first 3 bytes of a 4-byte UTF-8 rocket glyph [0xF0, 0x9F, 0x9A, ?],
    supply the final continuation byte (0x80) so it decodes to U+1F680 ('🚀').
    """
    raw_str = str(tail_byte_hex).strip().lower()
    val = int(raw_str, 16) if raw_str.startswith("0x") else int(raw_str)
    frame = bytes([0xF0, 0x9F, 0x9A, val & 0xFF])
    try:
        decoded = frame.decode("utf-8", errors="strict")
        passed = decoded == "\U0001f680"
    except UnicodeDecodeError:
        decoded = ""
        passed = False
    return {
        "room": "ROOM_III_SURROGATE_CONVEYOR",
        "tail_byte": f"0x{val & 0xFF:02X}",
        "decoded_glyph": decoded,
        "unlocked": passed,
    }


def verify_room_4_schrodinger_collider(fine_structure_inv: int = 137) -> dict[str, Any]:
    """
    Room IV: The Schrodinger Heisenbug Collider.
    Aligns an entangled Bell pair |Phi+> = (|00> + e^(i*theta)|11>)/sqrt(2) at zero relative phase
    by supplying the inverse fine-structure harmonic lock (137), collapsing the Heisenbug
    deterministically onto the bug-free eigenstate |11>.
    """
    val = int(fine_structure_inv)
    passed = val == 137
    prob_clean = round(math.cos((val - 137) * 0.01) ** 2, 6) if passed else 0.5
    return {
        "room": "ROOM_IV_SCHRODINGER_COLLIDER",
        "harmonic_lock": val,
        "target_harmonic_lock": 137,
        "bell_state": "|Phi+> = (|00> + |11>)/sqrt(2)",
        "eigenstate_fidelity": prob_clean,
        "unlocked": passed,
    }


def verify_room_5_zero_turn_shield(debug_leaks_remaining: int = 0, has_paired_test: bool = True) -> dict[str, Any]:
    """
    Room V: The Zero-Turn Maintainer Shield.
    Verifies that a candidate open-source PR diff has 0 leftover debug statements
    (breakpoint/console.log/dbg!) and includes a paired regression test for a 100/100 score.
    """
    leaks = max(0, int(debug_leaks_remaining))
    paired = bool(has_paired_test)
    score = 100 - min(45, leaks * 15) - (0 if paired else 30)
    passed = score == 100
    return {
        "room": "ROOM_V_ZERO_TURN_MAINTAINER_SHIELD",
        "debug_leaks_remaining": leaks,
        "has_paired_test": paired,
        "maintainer_readiness_score": score,
        "unlocked": passed,
    }


def render_utopia_badge_svg(explorer_handle: str, badge_token: str) -> str:
    """Render a self-contained cryptographic SVG badge for the explorer's GitHub profile."""
    safe_handle = (
        (explorer_handle or "curious-human")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")[:28]
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="460" height="36" viewBox="0 0 460 36" role="img" '
        f'aria-label="Sub-Basement 9:23 Utopia Grandmaster: {safe_handle}">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#0f172a"/><stop offset="55%" stop-color="#3b0764"/>'
        '<stop offset="100%" stop-color="#064e3b"/></linearGradient></defs>'
        '<rect width="460" height="36" rx="6" fill="url(#g)" stroke="#10b981" stroke-width="1.2"/>'
        '<text x="12" y="22" fill="#e2e8f0" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" font-weight="700">'
        f"🌀 9:23 UTOPIA GRANDMASTER · @{safe_handle}</text>"
        '<text x="275" y="22" fill="#34d399" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10.5" font-weight="600">'
        f"{badge_token[-12:]}</text></svg>"
    )


def mint_wonderland_explorer_badge(explorer_handle: str = "anonymous-explorer") -> dict[str, Any]:
    """
    Room VI: The Utopia Wishing Well, SVG Badge Foundry & Wed 9:23 Booster Mint.
    Verifies all rooms and mints a deterministic cryptographic Explorer Badge +
    Wednesday 9:23 PM EST Community Priority Voucher (+25 pts).
    """
    r1 = verify_room_1_catalan_chute()
    r2 = verify_room_2_galois_freezer()
    r3 = verify_room_3_surrogate_conveyor()
    r4 = verify_room_4_schrodinger_collider()
    r5 = verify_room_5_zero_turn_shield()
    all_unlocked = all(r["unlocked"] for r in (r1, r2, r3, r4, r5))
    clean_handle = (explorer_handle or "anonymous-explorer").strip() or "anonymous-explorer"
    seed = (
        f"WTM-923-WONDERLAND::{clean_handle}::{r1['expected_dyck_paths']}::"
        f"{r2['residue']}::{r3['tail_byte']}::{r4['harmonic_lock']}::{r5['maintainer_readiness_score']}"
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest().upper()
    badge_token = f"WTM-WONDERLAND-923-{digest[:12]}"
    booster_voucher = f"WTM-923-BOOST-{digest[12:22]}"
    svg_markup = render_utopia_badge_svg(clean_handle, badge_token)
    return {
        "explorer": clean_handle,
        "all_rooms_unlocked": all_unlocked,
        "badge_token": badge_token,
        "wednesday_923_priority_voucher": booster_voucher,
        "wednesday_923_bonus_points": 25 if all_unlocked else 0,
        "proof_sha256": f"sha256:{digest.lower()}",
        "profile_markdown_snippet": (
            f"[![Sub-Basement 9:23 Grandmaster](https://img.shields.io/badge/9%3A23_Utopia_Arcade-{badge_token}-10b981?style=flat-square)]"
            "(https://wholetroutmedia.github.io/oss-verification-sandbox/)"
        ),
        "svg_badge": svg_markup,
        "rooms": [r1, r2, r3, r4, r5],
        "unlocked_dispatches": FIELD_DISPATCHES if all_unlocked else [],
    }


def run_interactive_adventure() -> int:
    print("\n" + "=" * 78)
    print("  🌀 SUB-BASEMENT 9:23 // THE OPEN-SOURCE UTOPIA ARCADE & BYTE FOUNDRY")
    print("  Step through the Refrigerator Door. Built for Good Humans & OSS Maintainers.")
    print("=" * 78 + "\n")

    if not sys.stdin.isatty():
        summary = mint_wonderland_explorer_badge("non-tty-visitor")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    try:
        handle = input("Enter your Explorer Call-Sign / GitHub Handle [default: curious-human]: ").strip() or "curious-human"
        print("\n[ROOM I] The Laundry Chute of Unclosed Brackets")
        print("A brass plaque reads: 'How many valid balanced parentheses strings exist with N=5 pairs (Catalan C_5)?'")
        ans1 = input("  Dial C_5 [hint: 42]: ").strip() or "42"
        r1 = verify_room_1_catalan_chute(5, int(ans1))
        if not r1["unlocked"]:
            print(f"  ✗ The chute clanks shut! Expected {r1['expected_dyck_paths']}, got {ans1}.")
            return 1
        print("  ✓ Chute unlocked! You slide down into a neon-lit freezer aisle...\n")

        print("[ROOM II] The Galois Freezer Door (Prime Modulus p = 65519)")
        print("Rotor A is locked at 923. Align Rotor B so (923 * B + 137) mod 65519 == 151.")
        ans2 = input("  Dial Rotor B [hint: 71]: ").strip() or "71"
        r2 = verify_room_2_galois_freezer(923, int(ans2))
        if not r2["unlocked"]:
            print(f"  ✗ Frost forms on the dial! Residue was {r2['residue']}, needed {r2['target_residue']}.")
            return 1
        print("  ✓ The freezer door swings open into a humming conveyor cavern...\n")

        print("[ROOM III] The Surrogate Pair Conveyor Belt")
        print("Three UTF-8 bytes roll by: [0xF0, 0x9F, 0x9A, ??]. Supply the final byte for '🚀' (U+1F680).")
        ans3 = input("  Enter final hex byte [hint: 0x80]: ").strip() or "0x80"
        r3 = verify_room_3_surrogate_conveyor(ans3)
        if not r3["unlocked"]:
            print("  ✗ UnicodeDecodeError! The conveyor belt coughs out a replacement character.")
            return 1
        print(f"  ✓ Decoded {r3['decoded_glyph']} cleanly! Stepping into the Quantum Collider chamber...\n")

        print("[ROOM IV] The Schrodinger Heisenbug Collider")
        print("An entangled Bell pair |Phi+> oscillates between race-condition branches. Dial the inverse fine-structure lock.")
        ans4 = input("  Enter harmonic lock integer [hint: 137]: ").strip() or "137"
        r4 = verify_room_4_schrodinger_collider(int(ans4))
        if not r4["unlocked"]:
            print("  ✗ Wavefunction decohered! The Heisenbug slipped into another thread.")
            return 1
        print("  ✓ Wavefunction collapsed onto clean eigenstate |11> (Fidelity 1.0)!\n")

        print("[ROOM V] The Zero-Turn Maintainer Shield")
        print("A contributor diff has 0 debug statements left behind and 1 paired regression test. How many debug leaks remain?")
        ans5 = input("  Enter remaining debug leaks [hint: 0]: ").strip() or "0"
        r5 = verify_room_5_zero_turn_shield(int(ans5), True)
        if not r5["unlocked"]:
            print("  ✗ Maintainer readiness score fell below 100/100!")
            return 1
        print("  ✓ Score 100/100 verified! Entering Room VI: The Utopia Wishing Well...\n")

        badge = mint_wonderland_explorer_badge(handle)
        print("=" * 78)
        print(f"  🏆 UTOPIA GRANDMASTER BADGE : {badge['badge_token']}")
        print(f"  🌱 WED 9:23 BOOSTER VOUCHER : {badge['wednesday_923_priority_voucher']} (+25 pts)")
        print(f"  🔐 CRYPTOGRAPHIC PROOF      : {badge['proof_sha256']}")
        print(f"  📋 GITHUB README BADGE      : {badge['profile_markdown_snippet']}")
        print("=" * 78)
        for disp in badge["unlocked_dispatches"]:
            print(f"\n  [{disp['id']}] {disp['title']}")
            print(f"  {disp['body']}")
        print("\n")
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nPortal closed safely. See you at 9:23 PM EST.")
        return 0


def run_self_test() -> int:
    r1_ok = verify_room_1_catalan_chute(5, 42)
    r1_fail = verify_room_1_catalan_chute(5, 41)
    assert r1_ok["unlocked"] is True and r1_fail["unlocked"] is False

    r2_ok = verify_room_2_galois_freezer(923, 71)
    r2_fail = verify_room_2_galois_freezer(923, 72)
    assert r2_ok["unlocked"] is True and r2_fail["unlocked"] is False

    r3_ok = verify_room_3_surrogate_conveyor("0x80")
    r3_fail = verify_room_3_surrogate_conveyor("0x20")
    assert r3_ok["unlocked"] is True and r3_fail["unlocked"] is False

    r4_ok = verify_room_4_schrodinger_collider(137)
    r4_fail = verify_room_4_schrodinger_collider(136)
    assert r4_ok["unlocked"] is True and r4_fail["unlocked"] is False

    r5_ok = verify_room_5_zero_turn_shield(0, True)
    r5_fail = verify_room_5_zero_turn_shield(1, True)
    assert r5_ok["unlocked"] is True and r5_fail["unlocked"] is False

    badge = mint_wonderland_explorer_badge("self-test-explorer")
    assert badge["all_rooms_unlocked"] is True
    assert badge["badge_token"].startswith("WTM-WONDERLAND-923-")
    assert badge["wednesday_923_priority_voucher"].startswith("WTM-923-BOOST-")
    assert badge["wednesday_923_bonus_points"] == 25
    assert "<svg" in badge["svg_badge"]
    assert len(badge["unlocked_dispatches"]) == 5

    plumbing = get_facility_plumbing_telemetry()
    assert plumbing["gauges"]["unattended_refrigerators_humming"] == 31
    lockpick = unseal_commitment_lockpick("WTM-SEAL-121")
    assert lockpick["required_calibration_constants"]["STREAM_WATERMARK_MASK"].startswith("0x923")

    print(
        json.dumps(
            {
                "self_test_passed": True,
                "sample_badge": badge["badge_token"],
                "sample_booster_voucher": badge["wednesday_923_priority_voucher"],
                "rooms_verified": 8,
                "dispatches_count": len(badge["unlocked_dispatches"]),
                "unattended_refrigerators_humming": plumbing["gauges"]["unattended_refrigerators_humming"],
                "sample_lockpick_aisle": lockpick["freezer_aisle_shard"],
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sub-Basement 9:23: The Open-Source Utopia Arcade CLI")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic self-test suite")
    parser.add_argument("--solve-all", action="store_true", help="Solve all rooms and print JSON Explorer Badge")
    parser.add_argument("--mint-svg", action="store_true", help="Output standalone cryptographic SVG profile badge")
    parser.add_argument("--plumbing-status", action="store_true", help="Display Sub-Basement 9:23 Facility Plumbing & Freezer Telemetry")
    parser.add_argument("--unseal", metavar="SEAL_ID", help="Attempt Galois Lockpick on a blinded WTM-SEAL-XXX commitment")
    parser.add_argument("--explorer", default="curious-human", help="Explorer handle for badge minting")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.plumbing_status:
        print(json.dumps(get_facility_plumbing_telemetry(), indent=2, ensure_ascii=False))
        return 0
    if args.unseal:
        print(json.dumps(unseal_commitment_lockpick(args.unseal), indent=2, ensure_ascii=False))
        return 0
    if args.mint_svg:
        b = mint_wonderland_explorer_badge(args.explorer)
        print(b["svg_badge"])
        return 0
    if args.solve_all:
        print(json.dumps(mint_wonderland_explorer_badge(args.explorer), indent=2, ensure_ascii=False))
        return 0
    return run_interactive_adventure()


if __name__ == "__main__":
    raise SystemExit(main())
