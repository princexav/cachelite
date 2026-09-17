import json
import os
from typing import Callable, Any, Optional

class WriteAheadLog:
    """Simple append-only log for durability."""
    def __init__(self, path: str):
        self.path = path

    def append(self, op: str, key: str, value: Any = None, expires_at: Optional[float] = None):
        entry = json.dumps({"op": op, "k": key, "v": value, "exp": expires_at})
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def replay(self, apply_fn: Callable[[str, str, Any, Optional[float]], None]):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    data = json.loads(stripped)
                    apply_fn(data["op"], data["k"], data.get("v"), data.get("exp"))
                except Exception:
                    continue

    def close(self):
        pass
