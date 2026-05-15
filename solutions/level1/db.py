class InMemoryDB:
    def __init__(self):
        # {key: {field: {"value": v, "expires_at": float('inf')}}}
        self._store = {}

    def set(self, key, field, value):
        if key not in self._store:
            self._store[key] = {}
        self._store[key][field] = {"value": value, "expires_at": float('inf')}

    def get(self, key, field):
        try:
            return self._store[key][field]["value"]
        except KeyError:
            return None

    def delete(self, key, field):
        try:
            del self._store[key][field]
            return True
        except KeyError:
            return False
