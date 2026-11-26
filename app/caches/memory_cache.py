from typing import Any, Optional

from app.caches.icache import ICache


class MemoryCache(ICache):
    def __init__(self):
        self.items = {}

    def get(self, key: str) -> Optional[Any]:
        return self.items.get(key)

    def set(self, key: str, value: Any) -> None:
        self.items[key] = value

    def remove(self, key: str) -> None:
        self.items.pop(key, None)
