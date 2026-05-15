# codesignal-prep

CodeSignal interview prep — in-memory database implemented progressively across levels.

## Level 1 — Basic In-Memory DB

Concepts: dict operations, key-value storage, prefix scanning.

- `set(key, value)` — store key/value
- `get(key)` — retrieve value or None
- `delete(key)` — remove key
- `keys()` — all keys
- `scan(prefix)` — keys matching prefix

## Level 2 — TTL Support

Concepts: time-based expiry, tuple storage, filtering expired entries.

Extends Level 1 with:
- `set(key, value, ttl=None)` — optional TTL in seconds
- `get(key)` — returns None if expired
- `keys()` — excludes expired keys
- `scan(prefix)` — excludes expired keys matching prefix

## Usage

```bash
python -m unittest level1/test_db.py
python -m unittest level2/test_db.py
```
