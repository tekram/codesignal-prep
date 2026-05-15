import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'level2'))
from db import InMemoryDB as Level2DB


class InMemoryDB(Level2DB):
    def _is_alive(self, entry, timestamp):
        # half-open interval: valid on [created_at, expires_at)
        return entry["expires_at"] > timestamp

    def set_at(self, key, field, value, timestamp):
        if key not in self._store:
            self._store[key] = {}
        self._store[key][field] = {"value": value, "expires_at": float('inf')}

    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        if key not in self._store:
            self._store[key] = {}
        self._store[key][field] = {"value": value, "expires_at": timestamp + ttl}

    def get_at(self, key, field, timestamp):
        try:
            entry = self._store[key][field]
            return entry["value"] if self._is_alive(entry, timestamp) else None
        except KeyError:
            return None

    def delete_at(self, key, field, timestamp):
        try:
            entry = self._store[key][field]
            if not self._is_alive(entry, timestamp):
                return False
            del self._store[key][field]
            return True
        except KeyError:
            return False

    def scan_at(self, key, timestamp):
        if key not in self._store:
            return []
        fields = self._store[key]
        alive = [(f, fields[f]["value"]) for f in sorted(fields) if self._is_alive(fields[f], timestamp)]
        return [f"{f}({v})" for f, v in alive]

    def scan_by_prefix_at(self, key, timestamp, prefix):
        if key not in self._store:
            return []
        fields = self._store[key]
        alive = [
            (f, fields[f]["value"])
            for f in sorted(fields)
            if f.startswith(prefix) and self._is_alive(fields[f], timestamp)
        ]
        return [f"{f}({v})" for f, v in alive]
