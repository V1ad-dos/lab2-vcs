from app.cache_manager import CacheManager
from app.caches.disk_cache import DiskCache
from app.caches.distributed_cache import DistributedCache
from app.caches.memory_cache import MemoryCache
from app.caches.redis_cache import RedisCache
from app.caches.ttl_cache import TTLCache
from app.logger import LoggingCache


def main():
    # Сборка сети зависимостей; LoggingCache — обёртка, CacheManager не меняется
    memory_cache = LoggingCache(MemoryCache(), "MemoryCache")
    disk_cache = LoggingCache(DiskCache("data/cache.json"), "DiskCache")
    redis_cache = LoggingCache(RedisCache("localhost:6379"), "RedisCache")
    ttl_cache = LoggingCache(TTLCache(default_ttl=5.0), "TTLCache")

    manager = CacheManager([memory_cache, disk_cache, redis_cache, ttl_cache])

    print("--- Работа с тремя кэшами ---")
    manager.set("user:1", "Иван Петров")
    print("Из менеджера:", manager.get("user:1"))

    # Данные остались только на диске - менеджер найдёт их по цепочке
    memory_cache.remove("user:1")
    print("После очистки памяти:", manager.get("user:1"))

    manager.remove("user:1")
    print("После удаления:", manager.get("user:1"))

    print("\n--- Добавляем DistributedCache (CacheManager не меняется) ---")
    distributed_cache = LoggingCache(DistributedCache(node_count=3), "DistributedCache")
    extended_manager = CacheManager(
        [memory_cache, disk_cache, redis_cache, ttl_cache, distributed_cache]
    )

    distributed_cache.set("order:101", "1500.50")
    print("Из менеджера:", extended_manager.get("order:101"))

    print("\n--- TTLCache (значение живёт ограниченное время) ---")
    demo_ttl = TTLCache(default_ttl=2.0)
    demo_ttl.set("session:1", "активна")
    print("Сразу после set:", demo_ttl.get("session:1"))


if __name__ == "__main__":
    main()
