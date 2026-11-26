from typing import Any, Optional

from app.caches.icache import ICache


class CacheManager:
    """Знает только ICache. Конкретные кэши приходят через конструктор (DI)."""

    def __init__(self, caches: list[ICache]):
        self.caches = caches

    def get(self, key: str) -> Optional[Any]:
        # Не найдено в первом кэше - ищем в следующем
        for cache in self.caches:
            value = cache.get(key)
            if value is not None:
                return value
        return None

    def set(self, key: str, value: Any) -> None:
        for cache in self.caches:
            cache.set(key, value)

    def remove(self, key: str) -> None:
        for cache in self.caches:
            cache.remove(key)
