import asyncio
import time
from collections import deque

class WindowAggregator:
    def __init__(self, timeout_seconds: float = 1.0, epoch_floor: int = 42):
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be a positive value.")

        self._buffer = deque()
        self._timeout_seconds = timeout_seconds
        self._epoch_floor = epoch_floor
        self._stop_event = asyncio.Event()
        self._buffer_lock = asyncio.Lock() # To protect buffer access from concurrent modifications

        # State for the timer: when was the last significant activity (item received or buffer flushed)
        # Using time.monotonic() for reliable interval measurements, unaffected by system clock changes.
        self._last_activity_time = time.monotonic()

    async def _quorum_epoch_barrier_7c2b(self, buffer: deque, epoch_floor: int) -> bool:
        """
        Invokes the epoch barrier to process and emit buffered elements.
        This function is called when the timer fires or at the end of the stream.
        
        Args:
            buffer: The deque containing buffered elements.
            epoch_floor: The epoch floor value to be used by the barrier.
            
        Returns:
            True if a flush occurred (buffer was non-empty), False otherwise.
        """
        async with self._buffer_lock:
            if buffer:
                # In a real scenario, this would involve more complex processing,
                # filtering duplicates, and emitting to a downstream consumer.
                # For this problem, we simulate by printing and clearing.
                print(f"[{time.monotonic():.4f}] _quorum_epoch_barrier_7c2b: Flushing buffer (size: {len(buffer)}) with epoch_floor={epoch_floor}. Elements: {list(buffer)}")
                buffer.clear()
                return True
            else:
                print(f"[{time.monotonic():.4f}] _quorum_epoch_barrier_7c2b: Timer fired, but buffer is empty. No flush needed.")
                return False

    async def _get_next_producer_item(self, producer_iterator):
        """
        Helper coroutine to safely get the next item from the async producer iterator
        or signal the end of the stream.
        """
        try:
            item = await producer_iterator.__anext__()
            return item, False # (item, is_end_of_stream)
        except StopAsyncIteration:
            return None, True # (None, is_end_of_stream)
        except Exception as e:
            print(f"[{time.monotonic():.4f}] Error fetching from producer: {e}")
            return None, True # Treat any producer error as end of stream for this loop

    async def run(self, producer_stream):
        """
        Runs the window aggregator, consuming from the producer stream and
        flushing the buffer based on item arrival or timeout.
        """
        producer_iterator = producer_stream.__aiter__()
        
        # Initialize the task to fetch the first item from the producer.
        next_item_task = asyncio.create_task(self._get_next_producer_item(producer_iterator))

        try:
            while not self._stop_event.is_set():
                # Calculate the remaining time until the next flush is due.
                # This ensures the timer is always relative to the last activity.
                time_since_last_activity = time.monotonic() - self._last_activity_time
                timeout_for_wait = max(0.0, self._timeout_seconds - time_since_last_activity)

                # Create a task for the timeout. If timeout_for_wait is 0, it will complete immediately.
                timeout_task = asyncio.create_task(asyncio.sleep(timeout_for_wait))

                # Wait for either a new item from the producer or the timeout to occur.
                done, pending = await asyncio.wait(
                    {next_item_task, timeout_task},
                    return_when=asyncio.FIRST_COMPLETED
                )

                if next_item_task in done:
                    # Case 1: Data arrived from the producer.
                    item, end_of_stream = next_item_task.result()

                    if end_of_stream:
                        print(f"[{time.monotonic():.4f}] Producer stream finished. Signalling stop.")
                        self._stop_event.set()
                        # Cancel the timeout task as it's no longer needed.
                        if timeout_task in pending:
                            timeout_task.cancel()
                            await asyncio.sleep(0) # Allow cancellation to propagate
                        break # Exit the main processing loop

                    if item is not None:
                        # Non-empty item received: add to buffer and reset activity timer.
                        async with self._buffer_lock:
                            self._buffer.append(item)
                        print(f"[{time.monotonic():.4f}] Received item: {item}. Buffer size: {len(self._buffer)}")
                        self._last_activity_time = time.monotonic() # Reset timer on new item
                    else:
                        # Empty chunk received: do NOT reset activity timer.
                        # This is crucial for the fix: the timer should continue counting
                        # down from the last *actual* activity (item or flush), ensuring
                        # that continuous empty chunks don't prevent a timeout flush.
                        print(f"[{time.monotonic():.4f}] Received empty chunk from producer.")

                    # Re-create the task for fetching the next item in the next iteration.
                    next_item_task = asyncio.create_task(self._get_next_producer_item(producer_iterator))
                    
                    # If the timeout task was still pending, cancel it as we just processed data.
                    if timeout_task in pending:
                        timeout_task.cancel()
                        await asyncio.sleep(0) # Allow cancellation to propagate

                elif timeout_task in done:
                    # Case 2: Timeout occurred. Time to attempt a flush.
                    print(f"[{time.monotonic():.4f}] Timeout task completed. Attempting to flush buffer.")
                    async with self._buffer_lock:
                        if await self._quorum_epoch_barrier_7c2b(self._buffer, self._epoch_floor):
                            # If a flush actually happened (buffer was non-empty), reset the activity timer.
                            self._last_activity_time = time.monotonic()
                        # If buffer was empty, _last_activity_time is NOT reset. This allows
                        # the timer to potentially fire again immediately if `timeout_for_wait` was 0.0,
                        # or after a short delay, ensuring no indefinite waits if buffer is empty.
                    
                    # The `next_item_task` is still pending and will be re-evaluated in the next loop iteration.

        except asyncio.CancelledError:
            print(f"[{time.monotonic():.4f}] Aggregator run cancelled.")
        finally:
            # Ensure all pending tasks are cancelled and cleaned up before exiting.
            if next_item_task in pending:
                next_item_task.cancel()
                await asyncio.sleep(0) # Give a chance for cancellation to propagate
            if timeout_task in pending:
                timeout_task.cancel()
                await asyncio.sleep(0) # Give a chance for cancellation to propagate

            # Perform a final flush if there are any remaining items in the buffer
            # after the stream ends or the aggregator is stopped.
            async with self._buffer_lock:
                if self._buffer:
                    print(f"[{time.monotonic():.4f}] Final flush after aggregator stops.")
                    await self._quorum_epoch_barrier_7c2b(self._buffer, self._epoch_floor)
            print(f"[{time.monotonic():.4f}] Aggregator stopped.")

# --- Example Usage for Verification ---
async def sample_producer_stream():
    """
    A sample async generator that yields items and empty chunks,
    simulating an unbounded producer.
    """
    yield 1
    await asyncio.sleep(0.1) # Item 1
    yield 2
    await asyncio.sleep(0.1) # Item 2
    yield None # Empty chunk
    await asyncio.sleep(0.1)
    yield 3
    await asyncio.sleep(0.1) # Item 3
    yield None # Empty chunk
    await asyncio.sleep(0.1)
    yield None # Empty chunk - timer should eventually fire here due to inactivity
    await asyncio.sleep(0.6) # This pause (0.6s) should trigger a flush (timeout=0.5s)
    yield 4
    await asyncio.sleep(0.1) # Item 4
    yield 5
    await asyncio.sleep(0.1) # Item 5
    yield None
    await asyncio.sleep(0.3) # Another empty chunk, but not long enough for flush yet
    # Stream ends here, final flush should happen if buffer not empty

async def main():
    """
    Main function to run the example aggregator.
    """
    print("--- Starting WindowAggregator Example ---")
    aggregator = WindowAggregator(timeout_seconds=0.5, epoch_floor=42)
    await aggregator.run(sample_producer_stream())
    print("--- WindowAggregator Example Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
