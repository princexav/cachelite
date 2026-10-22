# CacheLite Roadmap (20+ Hours Planned Work)

This roadmap outlines planned systems engineering improvements for `CacheLite`.

---

## 📍 Phase 1: Eviction Policies & Memory Management (6–8 Hours)
- [ ] **LFU (Least Frequently Used) Policy:** Implement frequency tracking with min-heap for frequency-based eviction.
- [ ] **Max Memory Threshold (Bytes):** Enforce strict RAM limits based on `sys.getsizeof` object measuring rather than raw key count.
- [ ] **Active TTL Sweeper:** Background daemon thread to proactively sweep and free expired keys instead of lazy check-on-read.

---

## 📍 Phase 2: Write-Ahead Log Compaction & Snapshots (6–8 Hours)
- [ ] **WAL Log Compactor:** Periodically rewrite the append-only log to deduplicate stale overwrites and delete tombstoned keys.
- [ ] **Binary Snapshot Engine (RDB format):** Fast binary dump of in-memory hash tables for sub-second restart recovery.
- [ ] **CRC32 Checksum Validation:** Detect and gracefully repair disk corruption in WAL files.

---

## 📍 Phase 3: Client Protocols & Benchmarks (6–8 Hours)
- [ ] **Redis RESP Protocol Server:** Expose a minimal TCP socket server allowing standard Redis CLI and client libraries to query CacheLite.
- [ ] **Performance Benchmarking Suite:** Microbenchmarks measuring ops/second across concurrent read/write workloads.
- [ ] **Namespace Partitioning:** Allow logical keyspace isolation across different application tenants.
