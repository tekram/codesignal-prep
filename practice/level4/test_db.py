import unittest
from db import InMemoryDB


class TestLevel4(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_backup_returns_record_count(self):
        self.db.set_at("r1", "f", "v", 0)
        self.db.set_at("r2", "f", "v", 0)
        self.assertEqual(self.db.backup(0), 2)

    def test_backup_excludes_empty_records(self):
        self.db.set_at("r1", "f", "v", 0)
        self.db.delete_at("r1", "f", 0)
        self.db.set_at("r2", "f", "v", 0)
        self.assertEqual(self.db.backup(0), 1)

    def test_backup_excludes_expired_records(self):
        self.db.set_at_with_ttl("r1", "f", "v", 0, 5)  # expires at 5
        self.db.set_at("r2", "f", "v", 0)
        self.assertEqual(self.db.backup(5), 1)  # r1 expired at t=5

    def test_restore_basic(self):
        self.db.set_at("r1", "f", "original", 0)
        self.db.backup(0)
        self.db.set_at("r1", "f", "changed", 10)
        self.db.restore(20, 0)
        self.assertEqual(self.db.get_at("r1", "f", 20), "original")

    def test_restore_ttl_recalculated(self):
        # set at t=0 with ttl=10 → expires at 10
        self.db.set_at_with_ttl("r1", "f", "v", 0, 10)
        self.db.backup(0)  # backup at t=0: remaining = 10 - 0 = 10
        # restore at t=100 from backup at t=0 → new expires = 100 + 10 = 110
        self.db.restore(100, 0)
        self.assertEqual(self.db.get_at("r1", "f", 109), "v")
        self.assertIsNone(self.db.get_at("r1", "f", 110))  # half-open

    def test_restore_drops_fields_expired_at_backup_time(self):
        self.db.set_at_with_ttl("r1", "f", "v", 0, 5)  # expires at 5
        self.db.backup(10)  # backup at t=10, field already expired
        self.db.restore(20, 10)
        self.assertIsNone(self.db.get_at("r1", "f", 20))

    def test_restore_picks_latest_backup_before_target(self):
        self.db.set_at("r1", "f", "v1", 0)
        self.db.backup(0)
        self.db.set_at("r1", "f", "v2", 5)
        self.db.backup(5)
        self.db.set_at("r1", "f", "v3", 10)
        # restore from latest backup at or before t=4 → that's backup at t=0
        self.db.restore(20, 4)
        self.assertEqual(self.db.get_at("r1", "f", 20), "v1")

    def test_restore_no_backup_before_target_is_noop(self):
        self.db.set_at("r1", "f", "current", 0)
        self.db.restore(10, 5)  # no backup exists at or before t=5
        self.assertEqual(self.db.get_at("r1", "f", 10), "current")

    def test_infinite_ttl_preserved_after_restore(self):
        self.db.set_at("r1", "f", "v", 0)  # no TTL
        self.db.backup(0)
        self.db.restore(100, 0)
        self.assertEqual(self.db.get_at("r1", "f", 999999), "v")


if __name__ == "__main__":
    unittest.main()
