# Level 5 — Concurrency (Thread-Safe DB)

**NOTE: Exact spec unknown — this is the best inference from Anthropic's email hint.**
Email says: "concurrency using the standard library and your choice of either asyncio or threading modules."

Most likely requirement: make the database thread-safe so concurrent reads/writes don't corrupt state.

## Expected Changes

Wrap existing operations with a lock so they're safe to call from multiple threads simultaneously.

### Option A — threading (simpler, recommended under time pressure)

```python
import threading

class InMemoryDB:
    def __init__(self):
        self._store = {}
        self._lock = threading.Lock()

    def set_at(self, key, field, value, timestamp):
        with self._lock:
            ...  # existing logic

    def get_at(self, key, field, timestamp):
        with self._lock:
            ...
```

### Option B — asyncio

```python
import asyncio

class InMemoryDB:
    def __init__(self):
        self._store = {}
        self._lock = asyncio.Lock()

    async def set_at(self, key, field, value, timestamp):
        async with self._lock:
            ...

    async def get_at(self, key, field, timestamp):
        async with self._lock:
            ...
```

## Decision: Pick ONE before the test

`threading.Lock` is simpler — no `async/await` changes needed throughout. Go with threading unless you're very comfortable with asyncio.

## Possible Additional Methods

May add concurrent-specific operations like:
- `execute_many(operations)` — run list of ops atomically
- `compare_and_set(key, field, expected, new_value)` — atomic CAS

## Key Patterns

```python
# threading — RLock if methods call each other
self._lock = threading.RLock()  # re-entrant: same thread can acquire twice

# read-write lock pattern (more concurrent reads)
import threading
self._rw_lock = threading.RLock()
# or use threading.Semaphore for bounded concurrency
```

## Time Target

< 15 minutes

## Run Tests

```bash
cd practice/level5
python -m unittest test_db.py -v
```
