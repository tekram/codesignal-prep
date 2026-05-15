# Level 6 — Advanced Concurrency

**NOTE: Exact spec unknown — best inference from Anthropic's email hint.**

Possible scenarios (prepare for any):

## Scenario A — Async Batch Operations

```python
async def execute_many(self, operations: list) -> list:
    """
    Execute list of (op_name, *args) tuples concurrently or sequentially.
    Return list of results in order.
    """
```

## Scenario B — Concurrent Read / Exclusive Write

Allow multiple simultaneous reads, but writes require exclusive access.

```python
import threading

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()

    def acquire_read(self):
        with self._read_lock:
            self._readers += 1
            if self._readers == 1:
                self._write_lock.acquire()

    def release_read(self):
        with self._read_lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_lock.release()
```

## Scenario C — Async Version of Full DB

All methods become `async def`, called with `await`. Same logic, just async.

```python
import asyncio

class InMemoryDB:
    async def set_at(self, key, field, value, timestamp):
        async with self._lock:
            ...
```

## Scenario D — Worker Queue / Task Processing

Process operations via a queue from multiple producers.

```python
import queue, threading

class InMemoryDB:
    def __init__(self):
        self._queue = queue.Queue()
        self._worker = threading.Thread(target=self._process, daemon=True)
        self._worker.start()

    def _process(self):
        while True:
            op, args, result_event, result_box = self._queue.get()
            result_box[0] = op(*args)
            result_event.set()
```

## Key stdlib to Know Cold

```python
import threading
threading.Lock()          # basic mutex
threading.RLock()         # re-entrant (same thread can re-acquire)
threading.Thread(target=f, args=(...), daemon=True)
threading.Event()         # .set(), .wait(), .is_set()
threading.Semaphore(n)    # bounded concurrency

import asyncio
asyncio.Lock()
asyncio.gather(*coros)    # run coroutines concurrently
asyncio.create_task(coro)
asyncio.Queue()

import queue
queue.Queue()             # thread-safe FIFO
```

## Time Target

< 15 minutes

## Run Tests

```bash
cd practice/level6
python -m unittest test_db.py -v
```
