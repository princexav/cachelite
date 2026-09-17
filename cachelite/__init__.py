"""CacheLite: Fast, thread-safe in-memory key-value cache with WAL and TTL."""

__version__ = "0.1.0"

from .store import CacheStore

__all__ = ["CacheStore"]
