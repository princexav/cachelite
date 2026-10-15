import unittest
import os
import time
import uuid
from cachelite.store import CacheStore

class TestCacheStore(unittest.TestCase):
    def setUp(self):
        self.wal_path = f"test_{uuid.uuid4().hex}.wal"

    def tearDown(self):
        if os.path.exists(self.wal_path):
            try:
                os.remove(self.wal_path)
            except OSError:
                pass

    def test_basic_set_get(self):
        cache = CacheStore(max_size=10, wal_path=self.wal_path)
        cache.set("foo", "bar")
        self.assertEqual(cache.get("foo"), "bar")
        self.assertIsNone(cache.get("nonexistent"))
        cache.close()

    def test_lru_eviction(self):
        cache = CacheStore(max_size=2)
        cache.set("a", 1)
        cache.set("b", 2)
        # Access 'a' so 'b' becomes LRU
        _ = cache.get("a")
        # Insert 'c', should evict 'b'
        cache.set("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)
        self.assertIsNone(cache.get("b"))
        cache.close()

    def test_ttl_expiration(self):
        cache = CacheStore(max_size=10)
        cache.set("quick", "expires", ttl_seconds=0.05)
        self.assertEqual(cache.get("quick"), "expires")
        time.sleep(0.08)
        self.assertIsNone(cache.get("quick"))
        cache.close()

    def test_wal_durability(self):
        cache1 = CacheStore(max_size=10, wal_path=self.wal_path)
        cache1.set("persisted", "value_123")
        cache1.close()

        cache2 = CacheStore(max_size=10, wal_path=self.wal_path)
        self.assertEqual(cache2.get("persisted"), "value_123")
        cache2.close()

if __name__ == "__main__":
    unittest.main()
