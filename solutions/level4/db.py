import copy, bisect, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'level3'))
from db import InMemoryDB as Level3DB


class InMemoryDB(Level3DB):
    def __init__(self):
        super().__init__()
        self._backups = []  # [(timestamp, snapshot), ...] sorted by timestamp

    def backup(self, timestamp):
        snapshot = copy.deepcopy(self._store)
        self._backups.append((timestamp, snapshot))
        # count records with at least one alive field
        count = sum(
            1 for fields in snapshot.values()
            if any(self._is_alive(e, timestamp) for e in fields.values())
        )
        return count

    def restore(self, timestamp, timestamp_to_restore):
        # find latest backup at or before timestamp_to_restore
        times = [b[0] for b in self._backups]
        idx = bisect.bisect_right(times, timestamp_to_restore) - 1
        if idx < 0:
            return
        _, snapshot = self._backups[idx]
        # rebase TTLs relative to restore time
        new_store = {}
        for key, fields in snapshot.items():
            new_store[key] = {}
            for field, entry in fields.items():
                if entry["expires_at"] == float('inf'):
                    new_expires = float('inf')
                else:
                    remaining = entry["expires_at"] - timestamp_to_restore
                    if remaining <= 0:
                        continue  # was expired at backup time
                    new_expires = timestamp + remaining
                new_store[key][field] = {"value": entry["value"], "expires_at": new_expires}
        self._store = new_store
