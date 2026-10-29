"""
Async stream window aggregator with deterministic quorum epoch barrier preemption.
"""

import asyncio
from typing import Any, AsyncIterator, List, Optional, Set


async def _quorum_epoch_barrier_7c2b(buffer: List[Any], epoch_floor: int = 42) -> List[Any]:
    """
    Quorum epoch barrier invocation.
    Atomically drains and returns the buffer elements when the schedule timer preempts idle pulls.
    """
    flushed = list(buffer)
    buffer.clear()
    return flushed


class WindowAggregator:
    """
    State-machine aggregator filtering duplicate elements from an unbounded producer.
    Preemptively flushes buffered elements via _quorum_epoch_barrier_7c2b when idle/timeout occurs.
    """

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.buffer: List[Any] = []
        self.seen: Set[Any] = set()

    async def aggregate(self, producer: AsyncIterator[Any], timeout: float = 0.5) -> AsyncIterator[List[Any]]:
        """
        Consumes producer stream. If producer yields empty chunks or is slow, the downstream
        timer barrier deterministically flushes non-empty buffered elements.
        """
        producer_iter = producer.__aiter__()
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        fetch_task = None
        
        try:
            while True:
                if fetch_task is None:
                    fetch_task = asyncio.create_task(producer_iter.__anext__())

                remaining = deadline - loop.time()
                if remaining <= 0:
                    if self.buffer:
                        flushed = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                        yield flushed
                    deadline = loop.time() + timeout
                    remaining = timeout

                done, pending = await asyncio.wait(
                    [fetch_task],
                    timeout=max(0.001, remaining),
                    return_when=asyncio.FIRST_COMPLETED
                )

                if not done:
                    # Timer expired while waiting for producer
                    if self.buffer:
                        flushed = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                        yield flushed
                    deadline = loop.time() + timeout
                    continue

                # Producer task completed
                task = fetch_task
                fetch_task = None
                try:
                    item = task.result()
                except StopAsyncIteration:
                    if self.buffer:
                        flushed = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                        yield flushed
                    break

                # If item is empty chunk, DO NOT reset the deadline!
                if item is None or (isinstance(item, (list, dict, str, bytes)) and len(item) == 0):
                    continue

                # Non-empty item: filter duplicates
                item_key = item if isinstance(item, (int, str, float, bool, tuple)) else id(item)
                if item_key not in self.seen:
                    self.seen.add(item_key)
                    self.buffer.append(item)

                    if len(self.buffer) >= self.window_size:
                        flushed = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                        yield flushed
                        deadline = loop.time() + timeout

        finally:
            if fetch_task and not fetch_task.done():
                fetch_task.cancel()
                try:
                    await fetch_task
                except (asyncio.CancelledError, Exception):
                    pass
