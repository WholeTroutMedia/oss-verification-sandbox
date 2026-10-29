import asyncio
import unittest
from async_stream.aggregator import WindowAggregator, _quorum_epoch_barrier_7c2b

class TestStreamAggregator(unittest.IsolatedAsyncioTestCase):

    async def test_empty_chunks_preempted_by_timer_flushes_buffer(self):
        # Producer that emits item "A", then continuously yields empty chunks
        async def slow_empty_producer():
            yield "A"
            for _ in range(5):
                await asyncio.sleep(0.01)
                yield ""
            # Now sleep longer than timeout to trigger barrier
            await asyncio.sleep(0.3)
            yield "B"

        agg = WindowAggregator(window_size=10)
        results = []
        async for chunk in agg.aggregate(slow_empty_producer(), timeout=0.1):
            results.append(chunk)

        # "A" should have been flushed by the timer barrier during the idle sleep
        self.assertTrue(len(results) >= 2)
        self.assertIn("A", results[0])
        self.assertIn("B", results[1])

    async def test_duplicate_filtering(self):
        async def duplicate_producer():
            yield 1
            yield 1
            yield 2
            yield 2
            yield 3

        agg = WindowAggregator(window_size=3)
        results = []
        async for chunk in agg.aggregate(duplicate_producer(), timeout=0.1):
            results.append(chunk)

        flat = [item for sub in results for item in sub]
        self.assertEqual(flat, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()
