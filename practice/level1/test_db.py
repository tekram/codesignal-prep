import unittest
from db import InMemoryDB


class TestLevel1(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_set_and_get(self):
        self.db.set("rec1", "name", "Alice")
        self.assertEqual(self.db.get("rec1", "name"), "Alice")

    def test_get_missing_key(self):
        self.assertIsNone(self.db.get("nope", "name"))

    def test_get_missing_field(self):
        self.db.set("rec1", "name", "Alice")
        self.assertIsNone(self.db.get("rec1", "age"))

    def test_overwrite_field(self):
        self.db.set("rec1", "name", "Alice")
        self.db.set("rec1", "name", "Bob")
        self.assertEqual(self.db.get("rec1", "name"), "Bob")

    def test_multiple_fields(self):
        self.db.set("rec1", "name", "Alice")
        self.db.set("rec1", "age", "30")
        self.assertEqual(self.db.get("rec1", "name"), "Alice")
        self.assertEqual(self.db.get("rec1", "age"), "30")

    def test_delete_existing(self):
        self.db.set("rec1", "name", "Alice")
        self.assertTrue(self.db.delete("rec1", "name"))
        self.assertIsNone(self.db.get("rec1", "name"))

    def test_delete_missing_field(self):
        self.db.set("rec1", "name", "Alice")
        self.assertFalse(self.db.delete("rec1", "age"))

    def test_delete_missing_key(self):
        self.assertFalse(self.db.delete("nope", "name"))

    def test_multiple_records_independent(self):
        self.db.set("rec1", "name", "Alice")
        self.db.set("rec2", "name", "Bob")
        self.assertEqual(self.db.get("rec1", "name"), "Alice")
        self.assertEqual(self.db.get("rec2", "name"), "Bob")


if __name__ == "__main__":
    unittest.main()
