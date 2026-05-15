# Level 2 — TTL Support

Extend Level 1's `InMemoryDB` with time-to-live expiry.

## Methods (changes from Level 1)

```python
import time

class InMemoryDB:  # extends level1
    def set(self, key: str, value, ttl: float = None) -> None:
        # store key/value with optional TTL in seconds
        # if ttl given, key expires at time.time() + ttl

    def get(self, key: str):
        # return value, or None if missing OR expired

    def keys(self) -> list:
        # return only non-expired keys

    def scan(self, prefix: str) -> list:
        # return non-expired keys matching prefix
```

## Key Details

- Expired key behaves like it doesn't exist (get → None, delete → None)
- `set` without ttl → key never expires
- Overwriting an expired key with `set` should work normally
- No need to proactively clean up expired keys (lazy expiry is fine)

## Run Tests

```bash
python -m unittest practice/level2/test_db.py -v
```

## Time Target

< 15 minutes (including level 1 re-implementation or inheritance)

## Pattern to Remember

```python
# Store as tuple
self.store[key] = (value, time.time() + ttl if ttl else None)

# Check expiry
value, expires_at = self.store[key]
if expires_at is not None and time.time() > expires_at:
    return None  # expired
```
