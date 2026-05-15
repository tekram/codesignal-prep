import unittest
from db import InMemoryDB


class TestLevel2(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_scan_basic(self):
        self.db.set("rec1", "name", "Alice")
        self.db.set("rec1", "age", "30")
        self.assertEqual(self.db.scan("rec1"), ["age(30)", "name(Alice)"])

    def test_scan_sorted_lexicographically(self):
        self.db.set("rec1", "z", "last")
        self.db.set("rec1", "a", "first")
        self.db.set("rec1", "m", "mid")
        self.assertEqual(self.db.scan("rec1"), ["a(first)", "m(mid)", "z(last)"])

    def test_scan_missing_key(self):
        self.assertEqual(self.db.scan("nope"), [])

    def test_scan_single_field(self):
        self.db.set("rec1", "x", "val")
        self.assertEqual(self.db.scan("rec1"), ["x(val)"])

    def test_scan_by_prefix_match(self):
        self.db.set("rec1", "name", "Alice")
        self.db.set("rec1", "nickname", "Al")
        self.db.set("rec1", "age", "30")
        result = self.db.scan_by_prefix("rec1", "na")
        self.assertEqual(result, ["name(Alice)", "nickname(Al)"])

    def test_scan_by_prefix_no_match(self):
        self.db.set("rec1", "name", "Alice")
        self.assertEqual(self.db.scan_by_prefix("rec1", "xyz"), [])

    def test_scan_by_prefix_empty_prefix(self):
        self.db.set("rec1", "b", "2")
        self.db.set("rec1", "a", "1")
        self.assertEqual(self.db.scan_by_prefix("rec1", ""), ["a(1)", "b(2)"])

    def test_scan_by_prefix_missing_key(self):
        self.assertEqual(self.db.scan_by_prefix("nope", "a"), [])

    def test_scan_format_exact(self):
        self.db.set("r", "field", "value")
        self.assertEqual(self.db.scan("r"), ["field(value)"])


if __name__ == "__main__":
    unittest.main()
