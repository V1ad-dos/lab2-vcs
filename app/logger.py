"""Настройка logging и обёртка LoggingCache без изменения CacheManager."""

import logging
from typing import Any, Optional

from app.caches.icache import ICache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("cache")


class LoggingCache(ICache):
    """Декоратор ICache: логирует get/set/remove и делегирует вложенному кэшу."""

    def __init__(self, cache: ICache, name: Optional[str] = None):
        self._cache = cache
        self._name = name or type(cache).__name__

    def get(self, key: str) -> Optional[Any]:
        value = self._cache.get(key)
        logger.info("%s.get(%r) -> %r", self._name, key, value)
        return value

    def set(self, key: str, value: Any) -> None:
        logger.info("%s.set(%r, %r)", self._name, key, value)
        self._cache.set(key, value)

    def remove(self, key: str) -> None:
        logger.info("%s.remove(%r)", self._name, key)
        self._cache.remove(key)
