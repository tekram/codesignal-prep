import unittest
from db import InMemoryDB


class TestLevel3(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    # set_at
    def test_set_at_and_get_at(self):
        self.db.set_at("r", "f", "v", 1)
        self.assertEqual(self.db.get_at("r", "f", 1), "v")
        self.assertEqual(self.db.get_at("r", "f", 100), "v")

    def test_set_at_missing(self):
        self.assertIsNone(self.db.get_at("r", "f", 1))

    # set_at_with_ttl — half-open [t, t+ttl)
    def test_ttl_alive_before_expiry(self):
        self.db.set_at_with_ttl("r", "f", "v", 5, 10)
        self.assertEqual(self.db.get_at("r", "f", 14), "v")

    def test_ttl_expired_at_expiry_time(self):
        self.db.set_at_with_ttl("r", "f", "v", 5, 10)
        # expires_at = 15, so t=15 is expired (half-open)
        self.assertIsNone(self.db.get_at("r", "f", 15))

    def test_ttl_expired_after(self):
        self.db.set_at_with_ttl("r", "f", "v", 5, 10)
        self.assertIsNone(self.db.get_at("r", "f", 20))

    def test_ttl_alive_at_set_time(self):
        self.db.set_at_with_ttl("r", "f", "v", 5, 10)
        self.assertEqual(self.db.get_at("r", "f", 5), "v")

    # delete_at
    def test_delete_at_alive(self):
        self.db.set_at("r", "f", "v", 1)
        self.assertTrue(self.db.delete_at("r", "f", 5))
        self.assertIsNone(self.db.get_at("r", "f", 6))

    def test_delete_at_expired(self):
        self.db.set_at_with_ttl("r", "f", "v", 1, 5)
        self.assertFalse(self.db.delete_at("r", "f", 10))

    def test_delete_at_missing(self):
        self.assertFalse(self.db.delete_at("r", "f", 1))

    # scan_at
    def test_scan_at_filters_expired(self):
        self.db.set_at_with_ttl("r", "a", "1", 0, 10)  # expires at 10
        self.db.set_at("r", "b", "2", 0)               # no expiry
        result = self.db.scan_at("r", 10)
        self.assertEqual(result, ["b(2)"])

    def test_scan_at_all_alive(self):
        self.db.set_at("r", "z", "3", 0)
        self.db.set_at("r", "a", "1", 0)
        self.assertEqual(self.db.scan_at("r", 0), ["a(1)", "z(3)"])

    def test_scan_at_missing_key(self):
        self.assertEqual(self.db.scan_at("nope", 0), [])

    # scan_by_prefix_at
    def test_scan_by_prefix_at_filters_expired(self):
        self.db.set_at_with_ttl("r", "name", "Alice", 0, 5)  # expires at 5
        self.db.set_at("r", "nickname", "Al", 0)
        result = self.db.scan_by_prefix_at("r", 5, "na")
        self.assertEqual(result, ["nickname(Al)"])

    def test_scan_by_prefix_at_no_match(self):
        self.db.set_at("r", "name", "Alice", 0)
        self.assertEqual(self.db.scan_by_prefix_at("r", 0, "xyz"), [])

    # overwrite expired field
    def test_overwrite_expired_field(self):
        self.db.set_at_with_ttl("r", "f", "old", 0, 5)
        self.db.set_at("r", "f", "new", 10)
        self.assertEqual(self.db.get_at("r", "f", 10), "new")


if __name__ == "__main__":
    unittest.main()
