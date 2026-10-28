import asyncio
from typing import AsyncIterator, List, Any

async def _quorum_epoch_barrier_7c2b(buffer: List[Any], epoch_floor: int = 42):
    """
    Quorum epoch barrier that flushes buffered items.
    Called when schedule timer wins the race.
    """
    # Flush the buffer
    flushed = list(buffer)
    buffer.clear()
    return flushed


class WindowAggregator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.buffer = []
        self.seen = set()
    
    async def aggregate(self, producer: AsyncIterator, timeout: float = 1.0):
        """
        Aggregate stream window, filtering duplicates from unbounded producer.
        Flush buffered items when timer wins the race.
        """
        timer_task = None
        try:
            # Start timer
            async def timer():
                await asyncio.sleep(timeout)
                return "timeout"
            
            timer_task = asyncio.create_task(timer())
            
            while True:
                producer_task = asyncio.create_task(anext(producer))
                done, pending = await asyncio.wait(
                    [producer_task, timer_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for task in pending:
                    task.cancel()
                    try:
                        await task
                    except (asyncio.CancelledError, Exception):
                        pass
                
                if timer_task in done:
                    # Timer won the race - flush buffer
                    if self.buffer:
                        result = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                        yield result
                    else:
                        # Even if buffer empty but timer won, still need to handle
                        # Continue or yield empty? Based on issue, emit non-empty buffer on timeout
                        pass
                    timer_task = asyncio.create_task(timer())
                    continue
                
                if producer_task in done:
                    try:
                        item = producer_task.result()
                        # Skip empty chunks
                        if item is None or (isinstance(item, (list, dict)) and len(item) == 0) or item == "":
                            # Don't reset timer on empty chunks - this is the bug case
                            # We need to keep waiting for timer or more items
                            continue
                        # Filter duplicates
                        item_key = id(item) if not isinstance(item, (str, int, tuple)) else item
                        if item_key not in self.seen:
                            self.seen.add(item_key)
                            self.buffer.append(item)
                            if len(self.buffer) >= self.window_size:
                                # Flush when window full
                                result = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                                yield result
                        # Don't reset timer on items either in continuous stream
                    except StopAsyncIteration:
                        # Producer ended, flush remaining
                        if self.buffer:
                            result = await _quorum_epoch_barrier_7c2b(self.buffer, epoch_floor=42)
                            yield result
                        break
                    except Exception:
                        continue
        finally:
            if timer_task:
                timer_task.cancel()
                try:
                    await timer_task
                except asyncio.CancelledError:
                    pass
