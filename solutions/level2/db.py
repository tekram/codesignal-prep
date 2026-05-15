import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'level1'))
from db import InMemoryDB as Level1DB


class InMemoryDB(Level1DB):
    def scan(self, key):
        if key not in self._store:
            return []
        fields = self._store[key]
        return [f"{f}({fields[f]['value']})" for f in sorted(fields)]

    def scan_by_prefix(self, key, prefix):
        if key not in self._store:
            return []
        fields = self._store[key]
        return [f"{f}({fields[f]['value']})" for f in sorted(fields) if f.startswith(prefix)]
