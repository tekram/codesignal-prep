# Tashfeen's CodeSignal Prep Progress

## Level Completion

- [x] Level 1 — Basic CRUD (concepts covered)
- [x] Level 2 — TTL Support (concepts covered)
- [x] Level 3 — Thread Safety (concepts covered)
- [ ] Level 4 — Backup & Restore
- [ ] Level 5 — Concurrency (deep dive)
- [ ] Level 6 — Advanced Concurrency

---

## What We've Covered

### Level 1 — Basic InMemoryDB
- `__init__` with `self.store = {}`
- `set(key, value)` — stores value in dict
- `get(key)` — returns `None` if key missing
- `delete(key)` — returns `True` or `None`
- `keys()` — returns all keys
- `scan(prefix)` — returns keys starting with prefix

### Level 2 — TTL Support
- `set(key, value, ttl=None)` — stores `(value, expires_at)` tuple
- `get(key)` — unpacks tuple, checks expiry before returning
- `keys()` — filters out expired keys
- `scan(prefix)` — filters expired keys + prefix match

**Key concepts:**
- `time.time()` for current epoch time
- `expires_at = time.time() + ttl` when TTL is provided
- `None` expiry means lives forever
- Check: `expires_at is None or time.time() < expires_at`

### Level 3 — Thread Safety
- `__init__` adds `self.lock = threading.Lock()`
- All methods wrapped in `with self.lock:`
- Even read methods (`get`, `keys`, `scan`) need the lock

**Key concept:** Without locks, two threads can interleave reads/writes and get corrupted state.

---

## Python Patterns Learned

| Pattern | Example |
|---------|---------|
| `self` reference | `self.store = {}` |
| Type hints | `def get(key: str) -> str \| None:` |
| Tuple unpacking | `value, expires_at = self.store[key]` |
| Dict membership | `if key not in self.store:` |
| String prefix check | `key.startswith(prefix)` |
| List comprehension | `[k for k in self.store if k.startswith(p)]` |
| Delete from dict | `del self.store[key]` |
| Context manager lock | `with self.lock:` |

---

## Still To Cover

- [ ] asyncio (alternative to threading)
- [ ] Reading and understanding `unittest` test files
- [ ] Timed mock run (full 90-min simulation)
- [ ] Level 4: `backup(timestamp)` / `restore(timestamp, t_to_restore)` with TTL rebase
- [ ] Level 5/6: concurrency patterns under time pressure

---

## Reminders for the Real Test

1. **Read all 6 levels first** (2 min) — design Level 1 to accommodate Level 5/6
2. **Half-open TTL**: `expires_at = t + ttl`, alive if `expires_at > timestamp` (strict `>`)
3. **Scan format**: `"field(value)"`, no spaces, sorted by field name
4. **Restore TTL rebase**: `remaining = expires_at_at_backup - t_to_restore`, then `new_expires = now + remaining`
5. **`delete` returns `False`** for missing/expired fields — not `None`
6. Stick to `threading.Lock` — simpler than asyncio under time pressure
