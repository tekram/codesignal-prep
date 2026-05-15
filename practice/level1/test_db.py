import unittest
from db import InMemoryDB


class TestInMemoryDB(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_set_and_get(self):
        self.db.set("a", 1)
        self.assertEqual(self.db.get("a"), 1)

    def test_get_missing(self):
        self.assertIsNone(self.db.get("missing"))

    def test_overwrite(self):
        self.db.set("a", 1)
        self.db.set("a", 2)
        self.assertEqual(self.db.get("a"), 2)

    def test_delete_existing(self):
        self.db.set("a", 1)
        result = self.db.delete("a")
        self.assertTrue(result)
        self.assertIsNone(self.db.get("a"))

    def test_delete_missing(self):
        self.assertIsNone(self.db.delete("missing"))

    def test_keys(self):
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.assertCountEqual(self.db.keys(), ["a", "b"])

    def test_keys_empty(self):
        self.assertEqual(self.db.keys(), [])

    def test_scan(self):
        self.db.set("foo1", 1)
        self.db.set("foo2", 2)
        self.db.set("bar1", 3)
        self.assertCountEqual(self.db.scan("foo"), ["foo1", "foo2"])

    def test_scan_no_match(self):
        self.db.set("abc", 1)
        self.assertEqual(self.db.scan("xyz"), [])

    def test_scan_empty_prefix(self):
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.assertCountEqual(self.db.scan(""), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
