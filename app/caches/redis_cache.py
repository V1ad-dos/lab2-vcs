from typing import Any, Optional

from app.caches.icache import ICache


class RedisCache(ICache):
    """Имитация Redis: словарь и сообщения о командах."""

    def __init__(self, host: str):
        self.host = host
        self.items = {}

    def get(self, key: str) -> Optional[Any]:
        print(f"  [Redis {self.host}] GET {key}")
        return self.items.get(key)

    def set(self, key: str, value: Any) -> None:
        print(f"  [Redis {self.host}] SET {key}")
        self.items[key] = value

    def remove(self, key: str) -> None:
        print(f"  [Redis {self.host}] DEL {key}")
        self.items.pop(key, None)
