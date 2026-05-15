import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'level1'))
from db import InMemoryDB as Level1DB


class InMemoryDB(Level1DB):
    def set(self, key, value, ttl=None):
        expires_at = time.time() + ttl if ttl is not None else None
        self.store[key] = (value, expires_at)

    def _is_expired(self, key):
        if key not in self.store:
            return True
        _, expires_at = self.store[key]
        if expires_at is not None and time.time() > expires_at:
            return True
        return False

    def get(self, key):
        if self._is_expired(key):
            return None
        value, _ = self.store[key]
        return value

    def delete(self, key):
        if key in self.store and not self._is_expired(key):
            del self.store[key]
            return True
        return None

    def keys(self):
        return [k for k in self.store if not self._is_expired(k)]

    def scan(self, prefix):
        return [k for k in self.store if not self._is_expired(k) and k.startswith(prefix)]
