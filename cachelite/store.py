import time
import threading
from typing import Any, Optional, Dict
from .wal import WriteAheadLog

class Node:
    def __init__(self, key: str, value: Any, expires_at: Optional[float] = None):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class CacheStore:
    def __init__(self, max_size: int = 1000, wal_path: Optional[str] = None):
        self.max_size = max_size
        self._map: Dict[str, Node] = {}
        self._lock = threading.RLock()
        
        # Doubly linked list sentinels (head <-> ... <-> tail)
        self.head = Node("__head__", None)
        self.tail = Node("__tail__", None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.wal = WriteAheadLog(wal_path) if wal_path else None
        if self.wal:
            self._recover()

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        first = self.head.next
        node.prev = self.head
        node.next = first
        self.head.next = node
        if first:
            first.prev = node

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None):
        with self._lock:
            now = time.time()
            expires_at = (now + ttl_seconds) if ttl_seconds else None

            if key in self._map:
                node = self._map[key]
                node.value = value
                node.expires_at = expires_at
                self._remove(node)
                self._add_to_front(node)
            else:
                if len(self._map) >= self.max_size:
                    # Evict least recently used (node before tail)
                    lru = self.tail.prev
                    if lru and lru != self.head:
                        self._remove(lru)
                        del self._map[lru.key]
                        if self.wal:
                            self.wal.append("DEL", lru.key)

                new_node = Node(key, value, expires_at)
                self._map[key] = new_node
                self._add_to_front(new_node)

            if self.wal:
                self.wal.append("SET", key, value, expires_at)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._map:
                return None
            node = self._map[key]
            # Check expiration
            if node.expires_at and time.time() > node.expires_at:
                self.delete(key)
                return None
            
            # Move to front (most recently used)
            self._remove(node)
            self._add_to_front(node)
            return node.value

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._map:
                node = self._map[key]
                self._remove(node)
                del self._map[key]
                if self.wal:
                    self.wal.append("DEL", key)
                return True
            return False

    def size(self) -> int:
        with self._lock:
            return len(self._map)

    def _recover(self):
        saved_wal = self.wal
        self.wal = None  # prevent re-logging during replay
        try:
            def apply(op: str, key: str, value: Any, exp: Optional[float]):
                now = time.time()
                if exp and now > exp:
                    return
                if op == "SET":
                    self.set(key, value, ttl_seconds=(exp - now) if exp else None)
                elif op == "DEL":
                    self.delete(key)
            saved_wal.replay(apply)
        finally:
            self.wal = saved_wal

    def close(self):
        if self.wal:
            self.wal.close()
