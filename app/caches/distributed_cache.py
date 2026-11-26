from typing import Any, Optional

from app.caches.icache import ICache


class DistributedCache(ICache):
    """Имитация распределённого кэша: ключ попадает на один из узлов."""

    def __init__(self, node_count: int):
        self.nodes = [{} for _ in range(node_count)]

    def get(self, key: str) -> Optional[Any]:
        return self._node_for(key).get(key)

    def set(self, key: str, value: Any) -> None:
        self._node_for(key)[key] = value

    def remove(self, key: str) -> None:
        self._node_for(key).pop(key, None)

    def _node_for(self, key: str) -> dict:
        return self.nodes[hash(key) % len(self.nodes)]
