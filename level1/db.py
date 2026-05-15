class InMemoryDB:
    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key, None)

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return True
        return None

    def keys(self):
        return list(self.store.keys())

    def scan(self, prefix):
        return [k for k in self.store if k.startswith(prefix)]
