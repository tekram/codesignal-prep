class InMemoryDB:
    def __init__(self):
        pass

    def set_at(self, key, field, value, timestamp):
        pass

    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        pass

    def get_at(self, key, field, timestamp):
        pass

    def delete_at(self, key, field, timestamp):
        pass

    def scan_at(self, key, timestamp):
        pass

    def scan_by_prefix_at(self, key, timestamp, prefix):
        pass

    def backup(self, timestamp):
        pass

    def restore(self, timestamp, timestamp_to_restore):
        pass
