# cache_simple.py
from __future__ import annotations

from abc import ABC, abstractmethod
from threading import RLock
from typing import Callable, Generic, Optional, TypeVar

from cachetools import TTLCache

K = TypeVar("K")
V = TypeVar("V")


class Cache(ABC, Generic[K, V]):
    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        ...

    @abstractmethod
    def set(self, key: K, value: V) -> None:
        ...

    @abstractmethod
    def delete(self, key: K) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    def get_or_set(self, key: K, factory: Callable[[], V]) -> V:
        val = self.get(key)
        if val is not None:
            return val
        val = factory()
        self.set(key, val)
        return val


class InMemoryTTLCache(Cache[K, V]):
    def __init__(self, maxsize: int = 1024, ttl: float = 600.0):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = RLock()

    def get(self, key: K) -> Optional[V]:
        with self._lock:
            return self._cache.get(key)

    def set(self, key: K, value: V) -> None:
        with self._lock:
            self._cache[key] = value

    def delete(self, key: K) -> None:
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def __contains__(self, key: K) -> bool:
        with self._lock:
            return key in self._cache
