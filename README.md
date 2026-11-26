# Проект ЛР №1 (версия из main)

## Цель
Показать сетевую структуру классов и слабую связность (DIP, внедрение зависимостей через конструктор).

## Структура проекта
```
Lab1/
  app/
    cache_manager.py       основной модуль
    caches/
      icache.py            абстракция
      memory_cache.py
      disk_cache.py
      redis_cache.py
      distributed_cache.py четвёртый компонент (расширение)
  data/                    файл кэша на диске
  diagrams/classes.puml    UML
  docs/                    текст методички
  main.py                  сборка сети и демонстрация
```

## Сеть зависимостей
Звезда с центром в `ICache`:
`CacheManager` -> `ICache` <- `MemoryCache`, `DiskCache`, `RedisCache`, `DistributedCache`.

## DI и расширяемость
- `CacheManager` получает `list[ICache]` в конструкторе и не знает конкретных классов.
- `get` идёт по списку: не нашли в первом кэше - ищем в следующем.
- `DistributedCache` добавляется только в `main.py`; `cache_manager.py` не менялся.
- Классов основного модуля, которые надо менять при новом кэше: 0.

## Запуск
```
.venv\Scripts\activate
python main.py
```

## Автор
Каллаур В. А., группа ИСТ-41

## Описание
Проект демонстрирует слабую связность через интерфейсы.
Система с сетевыми структурами классов.
