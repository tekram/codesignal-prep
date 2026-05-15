import unittest
import time
from db import InMemoryDB


class TestInMemoryDBWithTTL(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_set_and_get(self):
        self.db.set("a", 1)
        self.assertEqual(self.db.get("a"), 1)

    def test_get_missing(self):
        self.assertIsNone(self.db.get("missing"))

    def test_set_with_ttl_not_expired(self):
        self.db.set("a", 1, ttl=10)
        self.assertEqual(self.db.get("a"), 1)

    def test_set_with_ttl_expired(self):
        self.db.set("a", 1, ttl=0.01)
        time.sleep(0.05)
        self.assertIsNone(self.db.get("a"))

    def test_delete_existing(self):
        self.db.set("a", 1)
        result = self.db.delete("a")
        self.assertTrue(result)
        self.assertIsNone(self.db.get("a"))

    def test_delete_missing(self):
        self.assertIsNone(self.db.delete("missing"))

    def test_delete_expired(self):
        self.db.set("a", 1, ttl=0.01)
        time.sleep(0.05)
        self.assertIsNone(self.db.delete("a"))

    def test_keys_excludes_expired(self):
        self.db.set("a", 1, ttl=0.01)
        self.db.set("b", 2, ttl=10)
        time.sleep(0.05)
        self.assertEqual(self.db.keys(), ["b"])

    def test_keys_no_ttl(self):
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.assertCountEqual(self.db.keys(), ["a", "b"])

    def test_scan_excludes_expired(self):
        self.db.set("foo1", 1, ttl=0.01)
        self.db.set("foo2", 2, ttl=10)
        self.db.set("bar1", 3)
        time.sleep(0.05)
        self.assertEqual(self.db.scan("foo"), ["foo2"])

    def test_scan_no_match(self):
        self.db.set("abc", 1)
        self.assertEqual(self.db.scan("xyz"), [])

    def test_overwrite_extends_ttl(self):
        self.db.set("a", 1, ttl=0.01)
        time.sleep(0.05)
        self.db.set("a", 2, ttl=10)
        self.assertEqual(self.db.get("a"), 2)


if __name__ == "__main__":
    unittest.main()
