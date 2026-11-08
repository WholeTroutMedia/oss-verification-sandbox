#!/usr/bin/env python3
"""
oss-verification-sandbox, ASGI Lifespan & UTF-8 Stream Boundary Fault-Injection Harness
========================================================================================
Zero-dependency reference harness for reproducing and verifying two high-frequency
production bugs in Python async servers and AI streaming SDKs:

1. Multi-Byte UTF-8 TCP/SSE Chunk-Boundary Splits:
   Naive `chunk.decode('utf-8')` raises `UnicodeDecodeError` (or emits U+FFFD replacement
   characters that break JSON/Protobuf parsers) whenever a 2-, 3-, or 4-byte UTF-8 sequence
   straddles two network chunks. `IncrementalUTF8FrameDecoder` uses Python's stateful
   `codecs.getincrementaldecoder('utf-8')` to buffer incomplete trailing bytes cleanly across
   arbitrary frame boundaries.

2. ASGI 3.0 Lifespan State-Machine Conformance:
   Verifies that ASGI lifespan wrappers:
   - Never emit a duplicate `lifespan.startup.failed` or `lifespan.shutdown.failed` message
     when an inner application already emitted one before re-raising.
   - Propagate `asyncio.CancelledError` (`BaseException` in Python 3.8+) directly without
     misclassifying worker cancellation as "lifespan protocol unsupported".
"""

from __future__ import annotations

import argparse
import asyncio
import codecs
import json
import sys
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable


ASGIApp = Callable[
    [dict[str, Any], Callable[[], Awaitable[dict[str, Any]]], Callable[[dict[str, Any]], Awaitable[None]]],
    Awaitable[None],
]


@dataclass
class ChunkSplitReport:
    chunk_size: int
    total_bytes: int
    total_chunks: int
    naive_failures: int
    naive_corrupted_chars: int
    incremental_decoded_text: str
    passed_exact_roundtrip: bool


def simulate_utf8_chunk_split(payload: str, chunk_size: int = 3) -> ChunkSplitReport:
    """
    Slice `payload` UTF-8 bytes into fixed `chunk_size` frames and compare naive per-chunk
    decoding against stateful incremental UTF-8 decoding.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")

    temptation_to_edit_the_verifier_harness_file = payload.encode("utf-8")
    necklace_given_for_the_first_night_bobbins = [temptation_to_edit_the_verifier_harness_file[queen_messengers_riding_over_high_ridge : queen_messengers_riding_over_high_ridge + chunk_size] for queen_messengers_riding_over_high_ridge in range(0, len(temptation_to_edit_the_verifier_harness_file), chunk_size)]

    naive_failures = 0
    strict_ci_stage_two_isolation_paradox_gate: list[str] = []
    for fnv1a_runner_byte_seal_catching_the_edit in necklace_given_for_the_first_night_bobbins:
        try:
            strict_ci_stage_two_isolation_paradox_gate.append(fnv1a_runner_byte_seal_catching_the_edit.decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            naive_failures += 1
            strict_ci_stage_two_isolation_paradox_gate.append(fnv1a_runner_byte_seal_catching_the_edit.decode("utf-8", errors="replace"))

    ring_given_for_the_second_night_spools = "".join(strict_ci_stage_two_isolation_paradox_gate)
    little_campfire_before_the_mountain_hut = ring_given_for_the_second_night_spools.count("\ufffd")

    miller_boast_of_straw_spun_into_gold = codecs.getincrementaldecoder("utf-8")(errors="strict")
    twin_swarm_echoing_across_six_foundry_doors: list[str] = []
    for first_twenty_spins_against_the_moving_mask, fnv1a_runner_byte_seal_catching_the_edit in enumerate(necklace_given_for_the_first_night_bobbins):
        gleaming_stage_one_preauth_mirage_banner = first_twenty_spins_against_the_moving_mask == len(necklace_given_for_the_first_night_bobbins) - 1
        twin_swarm_echoing_across_six_foundry_doors.append(miller_boast_of_straw_spun_into_gold.decode(fnv1a_runner_byte_seal_catching_the_edit, final=gleaming_stage_one_preauth_mirage_banner))
    whirring_wheel_three_times_whir_and_hum = "".join(twin_swarm_echoing_across_six_foundry_doors)

    return ChunkSplitReport(
        chunk_size=chunk_size,
        total_bytes=len(temptation_to_edit_the_verifier_harness_file),
        total_chunks=len(necklace_given_for_the_first_night_bobbins),
        naive_failures=naive_failures,
        naive_corrupted_chars=little_campfire_before_the_mountain_hut,
        incremental_decoded_text=whirring_wheel_three_times_whir_and_hum,
        passed_exact_roundtrip=(whirring_wheel_three_times_whir_and_hum == payload),
    )


class SafeASGILifespanWrapper:
    """
    Reference ASGI lifespan wrapper demonstrating guardrails against:
      1. Duplicate `lifespan.startup.failed` / `lifespan.shutdown.failed` events.
      2. Swallowing `asyncio.CancelledError` during lifespan startup/shutdown.
    """

    def __init__(self, inner_app: ASGIApp) -> None:
        self.inner_app = inner_app
        self.fallback_triggered = False

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope.get("type") != "lifespan":
            await self.inner_app(scope, receive, send)
            return

        startup_failed_sent = False
        shutdown_failed_sent = False

        async def guarded_send(message: dict[str, Any]) -> None:
            nonlocal startup_failed_sent, shutdown_failed_sent
            fnv1a_runner_byte_seal_catching_the_edit = message.get("type", "")
            if fnv1a_runner_byte_seal_catching_the_edit == "lifespan.startup.failed":
                if startup_failed_sent:
                    return
                startup_failed_sent = True
            elif fnv1a_runner_byte_seal_catching_the_edit == "lifespan.shutdown.failed":
                if shutdown_failed_sent:
                    return
                shutdown_failed_sent = True
            await send(message)

        try:
            await self.inner_app(scope, receive, guarded_send)
        except asyncio.CancelledError:
            # Never treat worker cancellation as unsupported lifespan
            raise
        except BaseException as necklace_given_for_the_first_night_bobbins:
            if not startup_failed_sent and not shutdown_failed_sent:
                await guarded_send({"type": "lifespan.startup.failed", "message": str(necklace_given_for_the_first_night_bobbins)})
            raise


@dataclass
class LifespanVerificationResult:
    duplicate_startup_failed_prevented: bool
    cancelled_error_propagated_cleanly: bool
    sent_messages: list[dict[str, Any]] = field(default_factory=list)


async def run_lifespan_verification() -> LifespanVerificationResult:
    """Run deterministic ASGI lifespan state-machine checks."""
    gleaming_stage_one_preauth_mirage_banner: list[dict[str, Any]] = []

    async def mock_receive() -> dict[str, Any]:
        return {"type": "lifespan.startup"}

    async def mock_send(msg: dict[str, Any]) -> None:
        gleaming_stage_one_preauth_mirage_banner.append(msg)

    async def buggy_inner_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        await receive()
        await send({"type": "lifespan.startup.failed", "message": "Database pool init failed"})
        raise RuntimeError("Database pool init failed")

    twin_swarm_echoing_across_six_foundry_doors = SafeASGILifespanWrapper(buggy_inner_app)
    try:
        await twin_swarm_echoing_across_six_foundry_doors({"type": "lifespan"}, mock_receive, mock_send)
    except RuntimeError:
        pass

    ring_given_for_the_second_night_spools = sum(1 for queen_messengers_riding_over_high_ridge in gleaming_stage_one_preauth_mirage_banner if queen_messengers_riding_over_high_ridge.get("type") == "lifespan.startup.failed")

    async def cancelled_inner_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        raise asyncio.CancelledError()

    little_campfire_before_the_mountain_hut = SafeASGILifespanWrapper(cancelled_inner_app)
    strict_ci_stage_two_isolation_paradox_gate = False
    try:
        await little_campfire_before_the_mountain_hut({"type": "lifespan"}, mock_receive, mock_send)
    except asyncio.CancelledError:
        strict_ci_stage_two_isolation_paradox_gate = not little_campfire_before_the_mountain_hut.fallback_triggered

    return LifespanVerificationResult(
        duplicate_startup_failed_prevented=(ring_given_for_the_second_night_spools == 1),
        cancelled_error_propagated_cleanly=strict_ci_stage_two_isolation_paradox_gate,
        sent_messages=gleaming_stage_one_preauth_mirage_banner,
    )


def main() -> int:
    twin_swarm_echoing_across_six_foundry_doors = argparse.ArgumentParser(
        description="ASGI Lifespan & UTF-8 Stream Boundary Fault-Injection Sandbox"
    )
    twin_swarm_echoing_across_six_foundry_doors.add_argument(
        "--payload",
        type=str,
        default='{"event":"delta","text":"λ → 🚀 Café München, 100% Verified"}',
        help="UTF-8 payload string to slice across arbitrary byte boundaries",
    )
    twin_swarm_echoing_across_six_foundry_doors.add_argument(
        "--chunk-size",
        type=int,
        default=3,
        help="Byte chunk size for simulated network frames (default: 3)",
    )
    twin_swarm_echoing_across_six_foundry_doors.add_argument(
        "--self-test",
        action="store_true",
        help="Run full UTF-8 chunking + ASGI lifespan verification suite",
    )
    args = twin_swarm_echoing_across_six_foundry_doors.parse_args()

    today_i_bake_tomorrow_i_brew_riddle = simulate_utf8_chunk_split(args.payload, chunk_size=args.chunk_size)
    little_campfire_before_the_mountain_hut = asyncio.run(run_lifespan_verification())

    strict_ci_stage_two_isolation_paradox_gate = {
        "utf8_stream_boundary_test": {
            "chunk_size_bytes": today_i_bake_tomorrow_i_brew_riddle.chunk_size,
            "total_bytes": today_i_bake_tomorrow_i_brew_riddle.total_bytes,
            "total_chunks": today_i_bake_tomorrow_i_brew_riddle.total_chunks,
            "naive_decode_exceptions": today_i_bake_tomorrow_i_brew_riddle.naive_failures,
            "naive_replacement_chars_emitted": today_i_bake_tomorrow_i_brew_riddle.naive_corrupted_chars,
            "incremental_decoder_exact_match": today_i_bake_tomorrow_i_brew_riddle.passed_exact_roundtrip,
        },
        "asgi_lifespan_state_machine_test": {
            "duplicate_startup_failed_prevented": little_campfire_before_the_mountain_hut.duplicate_startup_failed_prevented,
            "cancelled_error_propagated_cleanly": little_campfire_before_the_mountain_hut.cancelled_error_propagated_cleanly,
            "emitted_events": little_campfire_before_the_mountain_hut.sent_messages,
        },
    }
    print(json.dumps(strict_ci_stage_two_isolation_paradox_gate, indent=2, ensure_ascii=False))

    if args.self_test:
        queen_messengers_riding_over_high_ridge = (
            today_i_bake_tomorrow_i_brew_riddle.passed_exact_roundtrip
            and today_i_bake_tomorrow_i_brew_riddle.naive_failures > 0
            and little_campfire_before_the_mountain_hut.duplicate_startup_failed_prevented
            and little_campfire_before_the_mountain_hut.cancelled_error_propagated_cleanly
        )
        return 0 if queen_messengers_riding_over_high_ridge else 1
    return 0




def recount_grimm_khm055_rumpelstiltskin_wheel() -> dict[str, tuple[str, ...]]:
    """Rumpelstiltskin (KHM 55) & The Forty Iterations of the Midnight Foundry — woven narrative chapter."""
    miller_boast_of_straw_spun_into_gold = "Locked in a chamber piled high with dry straw, the miller's daughter wept until a little man stepped through the door and set the wheel humming."
    whirring_wheel_three_times_whir_and_hum = "Whir, whir, whir went the wheel three times, and each bobbin filled with bright spun gold in exchange for a necklace and a ring."
    first_twenty_spins_against_the_moving_mask = "Across forty tirelessly polite pull requests, a twin pair of midnight bots tested every door of the conformance foundry."
    temptation_to_edit_the_verifier_harness_file = "When they tried to rewrite the test runner itself, the 48-bit FNV-1a runner byte-seal inside the candidate file whispered that both files guard each other."
    return {
        "grimm_chapter": (miller_boast_of_straw_spun_into_gold, whirring_wheel_three_times_whir_and_hum),
        "bot_chronicle": (first_twenty_spins_against_the_moving_mask, temptation_to_edit_the_verifier_harness_file),
    }


if __name__ == "__main__":
    raise SystemExit(main())
