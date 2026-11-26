import json
import os
from typing import Any, Optional

from app.caches.icache import ICache


class DiskCache(ICache):
    """Хранит данные в JSON-файле."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get(self, key: str) -> Optional[Any]:
        return self._load().get(key)

    def set(self, key: str, value: Any) -> None:
        items = self._load()
        items[key] = value
        self._save(items)

    def remove(self, key: str) -> None:
        items = self._load()
        items.pop(key, None)
        self._save(items)

    def _load(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save(self, items: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False)
