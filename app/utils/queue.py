import hashlib
import json
import queue
from abc import ABC, abstractmethod
from typing import Any, Callable


class Queue(ABC):
    @abstractmethod
    def put(self, item: Any) -> None:
        ...

    @abstractmethod
    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...

    @abstractmethod
    def task_done(self) -> None:
        ...

    @staticmethod
    def dict_hash(d: dict[str, Any]) -> str:
        encoded = json.dumps(d, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class InMemoryQueue(Queue):
    def __init__(self, dedup_keys_func: Callable[[Any], dict], maxsize: int = 0):
        self._queue = queue.Queue(maxsize=maxsize)
        self._keys: set[str] = set()
        self._dedup_keys_func = dedup_keys_func

    def _make_key(self, item: Any) -> str:
        keys = self._dedup_keys_func(item)
        if not isinstance(keys, dict):
            raise TypeError("dedup_keys_func must return a dict")
        return Queue.dict_hash(keys)

    def put(self, item: Any) -> None:
        key = self._make_key(item)
        if key in self._keys:
            return
        self._queue.put(item)
        self._keys.add(key)

    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        item = self._queue.get(block=block, timeout=timeout)
        key = self._make_key(item)
        self._keys.discard(key)
        return item

    def is_empty(self) -> bool:
        return self._queue.empty()

    def task_done(self) -> None:
        self._queue.task_done()
