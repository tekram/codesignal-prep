# Level 3 — Timestamps + TTL

Extends Level 2. All prior operations get `_at` variants using integer timestamps.

## New Methods

```python
def set_at(self, key: str, field: str, value: str, timestamp: int) -> None:
    """Set field at given timestamp. No expiry."""

def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> None:
    """Set field at timestamp with TTL. Expires at timestamp + ttl (exclusive)."""

def get_at(self, key: str, field: str, timestamp: int) -> str | None:
    """Get field value at timestamp. None if missing or expired."""

def delete_at(self, key: str, field: str, timestamp: int) -> bool:
    """Delete field if alive at timestamp. Return True/False."""

def scan_at(self, key: str, timestamp: int) -> list[str]:
    """scan() but only non-expired fields at timestamp."""

def scan_by_prefix_at(self, key: str, timestamp: int, prefix: str) -> list[str]:
    """scan_by_prefix() but only non-expired fields at timestamp."""
```

## TTL Semantics — CRITICAL

TTL uses a **half-open interval**: `[timestamp, timestamp + ttl)`

- Set at t=5, ttl=10 → expires at t=15
- Valid at t=14 ✓
- **Expired at t=15** ✗ (NOT valid at the expiry time itself)

```python
def _is_alive(self, entry, timestamp):
    return entry["expires_at"] > timestamp  # strictly greater than
```

## Storage Schema

Store each field as a dict so L1/L2 code needs minimal changes:

```python
self._store[key][field] = {"value": value, "expires_at": float('inf')}
# with TTL:
self._store[key][field] = {"value": value, "expires_at": timestamp + ttl}
```

TTL is **per-(key, field)** — not per key.

## Architecture Tip

L1's `set` → call `set_at(key, field, value, 0)` internally.
L2's `scan` → call `scan_at(key, 0)` internally.
This keeps logic in one place.

## Time Target

< 25 minutes

## Run Tests

```bash
cd practice/level3
python -m unittest test_db.py -v
```
