# Level 4 — Backup & Restore

Extends Level 3. Add snapshot-based backup and restore.

## New Methods

```python
def backup(self, timestamp: int) -> int:
    """
    Snapshot current state at timestamp.
    Returns count of records that have at least one non-expired field at timestamp.
    (Not field count — record count.)
    """

def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
    """
    Restore from latest backup at or before timestamp_to_restore.
    TTLs are recalculated: remaining = expires_at_at_backup - timestamp_to_restore
    new expires_at = timestamp + remaining
    Fields expired at backup time are dropped.
    """
```

## Backup Semantics

- Multiple backups allowed; stored sorted by timestamp
- `restore` picks the **latest** backup whose timestamp ≤ `timestamp_to_restore`
- No backup found → no-op

## TTL Recalculation on Restore — CRITICAL

```
At backup time (timestamp_to_restore):
  field has expires_at = 100, backup at t=80
  remaining = 100 - 80 = 20

After restore at timestamp=200:
  new expires_at = 200 + 20 = 220
```

Fields with `expires_at == float('inf')` stay infinite.
Fields already expired at backup time → drop (don't restore).

## Implementation Pattern

```python
import copy, bisect

def backup(self, timestamp):
    self._backups.append((timestamp, copy.deepcopy(self._store)))
    # count records with ≥1 alive field
    ...

def restore(self, timestamp, timestamp_to_restore):
    times = [b[0] for b in self._backups]
    idx = bisect.bisect_right(times, timestamp_to_restore) - 1
    if idx < 0:
        return
    _, snapshot = self._backups[idx]
    # rebase TTLs...
```

## Time Target

< 25 minutes

## Run Tests

```bash
cd practice/level4
python -m unittest test_db.py -v
```
