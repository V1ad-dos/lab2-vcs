from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Абстракция, от которой зависит CacheManager."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Вернуть значение или None, если ключа нет."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def remove(self, key: str) -> None:
        pass
