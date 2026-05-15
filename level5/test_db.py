"""
Tests for thread-safe InMemoryDB.
Verifies no data corruption under concurrent reads/writes.
"""
import unittest
import threading
from db import InMemoryDB


class TestLevel5Threading(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_basic_ops_still_work(self):
        self.db.set_at("r", "f", "v", 0)
        self.assertEqual(self.db.get_at("r", "f", 0), "v")

    def test_concurrent_writes_no_exception(self):
        errors = []
        def write(i):
            try:
                self.db.set_at(f"key{i}", "field", str(i), 0)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=write, args=(i,)) for i in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()

        self.assertEqual(errors, [])
        self.assertEqual(len([k for k in range(50) if self.db.get_at(f"key{k}", "field", 0) == str(k)]), 50)

    def test_concurrent_reads_no_exception(self):
        self.db.set_at("r", "f", "v", 0)
        errors = []
        results = []
        lock = threading.Lock()

        def read():
            try:
                val = self.db.get_at("r", "f", 0)
                with lock:
                    results.append(val)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=read) for _ in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()

        self.assertEqual(errors, [])
        self.assertTrue(all(r == "v" for r in results))

    def test_concurrent_read_write_no_corruption(self):
        self.db.set_at("shared", "counter", "0", 0)
        errors = []

        def writer(i):
            try:
                self.db.set_at("shared", f"field{i}", str(i), i)
            except Exception as e:
                errors.append(e)

        def reader():
            try:
                self.db.scan_at("shared", 0)
            except Exception as e:
                errors.append(e)

        threads = (
            [threading.Thread(target=writer, args=(i,)) for i in range(25)] +
            [threading.Thread(target=reader) for _ in range(25)]
        )
        for t in threads: t.start()
        for t in threads: t.join()

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
