"""Тесты TTLCache."""

import time

from app.cache_manager import CacheManager
from app.caches.memory_cache import MemoryCache
from app.caches.ttl_cache import TTLCache


def test_ttl_cache_returns_value_before_expiry():
    cache = TTLCache(default_ttl=5.0)
    cache.set("k", "v")
    assert cache.get("k") == "v"


def test_ttl_cache_returns_none_after_expiry():
    cache = TTLCache(default_ttl=0.05)
    cache.set("k", "v")
    time.sleep(0.08)
    assert cache.get("k") is None


def test_ttl_cache_remove():
    cache = TTLCache(default_ttl=60.0)
    cache.set("k", "v")
    cache.remove("k")
    assert cache.get("k") is None


def test_ttl_cache_works_with_cache_manager():
    memory = MemoryCache()
    ttl = TTLCache(default_ttl=60.0)
    manager = CacheManager([memory, ttl])
    ttl.set("temp", "ok")
    assert manager.get("temp") == "ok"
