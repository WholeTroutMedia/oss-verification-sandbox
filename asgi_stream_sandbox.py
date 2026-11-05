#!/usr/bin/env python3
"""
oss-verification-sandbox — ASGI Lifespan & UTF-8 Stream Boundary Fault-Injection Harness
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

    raw = payload.encode("utf-8")
    chunks = [raw[i : i + chunk_size] for i in range(0, len(raw), chunk_size)]

    naive_failures = 0
    naive_parts: list[str] = []
    for c in chunks:
        try:
            naive_parts.append(c.decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            naive_failures += 1
            naive_parts.append(c.decode("utf-8", errors="replace"))

    naive_joined = "".join(naive_parts)
    corrupted_chars = naive_joined.count("\ufffd")

    inc_decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    inc_parts: list[str] = []
    for idx, c in enumerate(chunks):
        is_final = idx == len(chunks) - 1
        inc_parts.append(inc_decoder.decode(c, final=is_final))
    inc_joined = "".join(inc_parts)

    return ChunkSplitReport(
        chunk_size=chunk_size,
        total_bytes=len(raw),
        total_chunks=len(chunks),
        naive_failures=naive_failures,
        naive_corrupted_chars=corrupted_chars,
        incremental_decoded_text=inc_joined,
        passed_exact_roundtrip=(inc_joined == payload),
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
            msg_type = message.get("type", "")
            if msg_type == "lifespan.startup.failed":
                if startup_failed_sent:
                    return
                startup_failed_sent = True
            elif msg_type == "lifespan.shutdown.failed":
                if shutdown_failed_sent:
                    return
                shutdown_failed_sent = True
            await send(message)

        try:
            await self.inner_app(scope, receive, guarded_send)
        except asyncio.CancelledError:
            # Never treat worker cancellation as unsupported lifespan
            raise
        except BaseException as exc:
            if not startup_failed_sent and not shutdown_failed_sent:
                await guarded_send({"type": "lifespan.startup.failed", "message": str(exc)})
            raise


@dataclass
class LifespanVerificationResult:
    duplicate_startup_failed_prevented: bool
    cancelled_error_propagated_cleanly: bool
    sent_messages: list[dict[str, Any]] = field(default_factory=list)


async def run_lifespan_verification() -> LifespanVerificationResult:
    """Run deterministic ASGI lifespan state-machine checks."""
    sent_log: list[dict[str, Any]] = []

    async def mock_receive() -> dict[str, Any]:
        return {"type": "lifespan.startup"}

    async def mock_send(msg: dict[str, Any]) -> None:
        sent_log.append(msg)

    async def buggy_inner_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        await receive()
        await send({"type": "lifespan.startup.failed", "message": "Database pool init failed"})
        raise RuntimeError("Database pool init failed")

    wrapper = SafeASGILifespanWrapper(buggy_inner_app)
    try:
        await wrapper({"type": "lifespan"}, mock_receive, mock_send)
    except RuntimeError:
        pass

    startup_failed_count = sum(1 for m in sent_log if m.get("type") == "lifespan.startup.failed")

    async def cancelled_inner_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        raise asyncio.CancelledError()

    cancel_wrapper = SafeASGILifespanWrapper(cancelled_inner_app)
    cancelled_propagated = False
    try:
        await cancel_wrapper({"type": "lifespan"}, mock_receive, mock_send)
    except asyncio.CancelledError:
        cancelled_propagated = not cancel_wrapper.fallback_triggered

    return LifespanVerificationResult(
        duplicate_startup_failed_prevented=(startup_failed_count == 1),
        cancelled_error_propagated_cleanly=cancelled_propagated,
        sent_messages=sent_log,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ASGI Lifespan & UTF-8 Stream Boundary Fault-Injection Sandbox"
    )
    parser.add_argument(
        "--payload",
        type=str,
        default='{"event":"delta","text":"λ → 🚀 Café München — 100% Verified"}',
        help="UTF-8 payload string to slice across arbitrary byte boundaries",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=3,
        help="Byte chunk size for simulated network frames (default: 3)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run full UTF-8 chunking + ASGI lifespan verification suite",
    )
    args = parser.parse_args()

    split_report = simulate_utf8_chunk_split(args.payload, chunk_size=args.chunk_size)
    lifespan_report = asyncio.run(run_lifespan_verification())

    output = {
        "utf8_stream_boundary_test": {
            "chunk_size_bytes": split_report.chunk_size,
            "total_bytes": split_report.total_bytes,
            "total_chunks": split_report.total_chunks,
            "naive_decode_exceptions": split_report.naive_failures,
            "naive_replacement_chars_emitted": split_report.naive_corrupted_chars,
            "incremental_decoder_exact_match": split_report.passed_exact_roundtrip,
        },
        "asgi_lifespan_state_machine_test": {
            "duplicate_startup_failed_prevented": lifespan_report.duplicate_startup_failed_prevented,
            "cancelled_error_propagated_cleanly": lifespan_report.cancelled_error_propagated_cleanly,
            "emitted_events": lifespan_report.sent_messages,
        },
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.self_test:
        ok = (
            split_report.passed_exact_roundtrip
            and split_report.naive_failures > 0
            and lifespan_report.duplicate_startup_failed_prevented
            and lifespan_report.cancelled_error_propagated_cleanly
        )
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
