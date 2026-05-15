"""
Thread-safe InMemoryDB using threading.RLock.
RLock chosen over Lock: methods can call each other without deadlock.
"""
import threading, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'level4'))
from db import InMemoryDB as Level4DB


class InMemoryDB(Level4DB):
    def __init__(self):
        super().__init__()
        self._lock = threading.RLock()

    def set_at(self, key, field, value, timestamp):
        with self._lock:
            super().set_at(key, field, value, timestamp)

    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        with self._lock:
            super().set_at_with_ttl(key, field, value, timestamp, ttl)

    def get_at(self, key, field, timestamp):
        with self._lock:
            return super().get_at(key, field, timestamp)

    def delete_at(self, key, field, timestamp):
        with self._lock:
            return super().delete_at(key, field, timestamp)

    def scan_at(self, key, timestamp):
        with self._lock:
            return super().scan_at(key, timestamp)

    def scan_by_prefix_at(self, key, timestamp, prefix):
        with self._lock:
            return super().scan_by_prefix_at(key, timestamp, prefix)

    def backup(self, timestamp):
        with self._lock:
            return super().backup(timestamp)

    def restore(self, timestamp, timestamp_to_restore):
        with self._lock:
            super().restore(timestamp, timestamp_to_restore)
