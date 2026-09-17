"""Bounded in-process queue. One worker, positional result contract, zero retries."""
import asyncio
import time

class QueueUnavailable(RuntimeError):
    pass

class BatchQueue:
    def __init__(self, process, max_batch=10, max_wait=.005, capacity=100, timeout=2):
        if max_batch < 1 or capacity < 1 or max_wait <= 0 or timeout <= 0:
            raise ValueError('positive batch configuration required')
        self.process = process
        self.max_batch, self.max_wait, self.timeout = max_batch, max_wait, timeout
        self.queue = asyncio.Queue(maxsize=capacity)
        self.task = None
        self.closed = False
        self.batch_sizes = []
        self.batches = self.items = self.failures = self.rejected = 0

    async def submit(self, message):
        if self.closed:
            raise QueueUnavailable('queue closed')
        if self.task is None:
            self.task = asyncio.create_task(self._run())
        future = asyncio.get_running_loop().create_future()
        try:
            self.queue.put_nowait((message, future, time.monotonic()))
        except asyncio.QueueFull:
            self.rejected += 1
            raise QueueUnavailable('queue full') from None
        # Bounds total queueing and processing latency. Cancellation propagates to future.
        return await asyncio.wait_for(future, self.timeout)

    @staticmethod
    def fail(rows, error):
        for _, future, _ in rows:
            if not future.done():
                future.set_exception(error)

    async def _run(self):
        active = []
        try:
            while True:
                active = [await self.queue.get()]
                deadline = active[0][2]+self.max_wait
                while len(active) < self.max_batch:
                    # Drain ready items even if an older item already waited its window.
                    try:
                        active.append(self.queue.get_nowait())
                        continue
                    except asyncio.QueueEmpty:
                        pass
                    remaining = deadline-time.monotonic()
                    if remaining <= 0:
                        break
                    try:
                        active.append(await asyncio.wait_for(self.queue.get(), remaining))
                    except TimeoutError:
                        break
                live = [row for row in active if not row[1].done()]
                if live:
                    self.batches += 1
                    self.items += len(live)
                    # Bounded history; cumulative counters remain complete.
                    self.batch_sizes = (self.batch_sizes+[len(live)])[-100:]
                    try:
                        results = await asyncio.wait_for(
                            self.process([row[0] for row in live]), self.timeout)
                        if len(results) != len(live):
                            raise ValueError('batch result count mismatch')
                        for (_, future, _), result in zip(live, results):
                            if not future.done():
                                future.set_result(result)
                    except Exception as exc:
                        self.failures += 1
                        self.fail(live, exc)
                for _ in active:
                    self.queue.task_done()
                active = []
        finally:
            self.fail(active, QueueUnavailable('worker stopped'))
            for _ in active:
                self.queue.task_done()
            while not self.queue.empty():
                row = self.queue.get_nowait()
                self.fail([row], QueueUnavailable('worker stopped'))
                self.queue.task_done()

    async def close(self):
        self.closed = True
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        # Handles shutdown before the newly created worker first runs.
        while not self.queue.empty():
            self.fail([self.queue.get_nowait()], QueueUnavailable('queue closed'))
            self.queue.task_done()
