"""Кэш со временем жизни значений (TTL)."""

import time
from typing import Any, Optional

from app.caches.icache import ICache


class TTLCache(ICache):
    """Хранит значения с TTL; просроченные ключи возвращают None."""

    def __init__(self, default_ttl: float = 60.0):
        self.default_ttl = default_ttl
        self._items = {}  # type: dict[str, tuple[Any, float]]

    def get(self, key: str) -> Optional[Any]:
        entry = self._items.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.monotonic() >= expires_at:
            self._items.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._items[key] = (value, time.monotonic() + self.default_ttl)

    def remove(self, key: str) -> None:
        self._items.pop(key, None)
