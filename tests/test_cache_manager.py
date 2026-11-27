"""Тесты CacheManager, расширяемости и LoggingCache."""

from app.cache_manager import CacheManager
from app.caches.disk_cache import DiskCache
from app.caches.distributed_cache import DistributedCache
from app.caches.memory_cache import MemoryCache
from app.caches.redis_cache import RedisCache
from app.logger import LoggingCache


def test_get_searches_cache_chain(tmp_path):
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    redis = RedisCache("localhost:6379")
    manager = CacheManager([memory, disk, redis])

    disk.set("user:1", "из диска")
    assert manager.get("user:1") == "из диска"


def test_set_writes_to_all_caches(tmp_path):
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    redis = RedisCache("localhost:6379")
    manager = CacheManager([memory, disk, redis])

    manager.set("key", "value")
    assert memory.get("key") == "value"
    assert disk.get("key") == "value"
    assert redis.get("key") == "value"


def test_remove_from_all_caches(tmp_path):
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    redis = RedisCache("localhost:6379")
    manager = CacheManager([memory, disk, redis])

    manager.set("key", "value")
    manager.remove("key")
    assert manager.get("key") is None
    assert memory.get("key") is None
    assert disk.get("key") is None
    assert redis.get("key") is None


def test_distributed_cache_extends_without_changing_manager():
    memory = MemoryCache()
    distributed = DistributedCache(node_count=3)
    manager = CacheManager([memory, distributed])

    distributed.set("order:101", "1500.50")
    assert manager.get("order:101") == "1500.50"


def test_logging_cache_delegates(tmp_path, caplog):
    import logging

    inner = MemoryCache()
    wrapped = LoggingCache(inner, "MemoryCache")
    manager = CacheManager([wrapped])

    with caplog.at_level(logging.INFO, logger="cache"):
        manager.set("a", "b")
        assert manager.get("a") == "b"
        manager.remove("a")

    assert manager.get("a") is None
    assert any("MemoryCache.set" in message for message in caplog.messages)
    assert any("MemoryCache.get" in message for message in caplog.messages)
    assert any("MemoryCache.remove" in message for message in caplog.messages)
