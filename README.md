# CacheLite ⚡

> An embedded, thread-safe in-memory key-value cache with Write-Ahead Logging (WAL) and TTL expiration.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 What is CacheLite?

When applications need high-throughput caching without the operational overhead of running a full Redis or Memcached server cluster, **CacheLite** provides an embedded alternative:

- **O(1) LRU Eviction:** Automatic memory management using a doubly-linked hash map to evict least-recently-used keys when capacity is reached.
- **Dynamic TTL Expiration:** Automatic expiration of keys after a configurable number of seconds.
- **Crash Durability (WAL):** Appends mutations to a Write-Ahead Log (`cache.wal`) on disk and automatically recovers state on restart.
- **Thread-Safe:** Protected by reader/writer reentrant locks for safe multi-threaded execution.

---

## 📦 Usage

```python
from cachelite import CacheStore

# Initialize cache with max 1000 items and disk persistence
cache = CacheStore(max_size=1000, wal_path="cache.wal")

# Set with 60 second TTL
cache.set("user:123", {"name": "Alice"}, ttl_seconds=60)

# Get value
user = cache.get("user:123")
print(user) # {"name": "Alice"}
```

---

## 🧪 Testing

```bash
python -m unittest discover -s tests
```

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for planned engineering milestones (LFU eviction, Redis RESP protocol server, log compactor).

## 📄 License

MIT License - see [LICENSE](LICENSE).
