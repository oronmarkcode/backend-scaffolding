import hashlib
import json
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable
from threading import Condition
from typing import Any, Optional


class Queue(ABC):
    @abstractmethod
    def put(self, item: Any) -> None:
        pass

    @abstractmethod
    def get(self) -> Optional[Any]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def task_done(self) -> None:
        pass

    @staticmethod
    def dict_hash(d: dict[str, Any]) -> str:
        encoded = json.dumps(d, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class InMemoryQueue(Queue):
    def __init__(self, dedup_keys_func: Callable[[dict[str, Any]], dict]) -> None:
        self._queue = deque()
        self._cv = Condition()
        self.deduplication_set = set()
        self.dedup_keys_func = dedup_keys_func

    def is_in_queue(self, item: Any):
        return (
            InMemoryQueue.dict_hash(self.dedup_keys_func(item))
            in self.deduplication_set
        )

    def put(self, item: Any) -> None:
        with self._cv:
            if self.is_in_queue(item):
                return
            self._queue.append(item)
            self.deduplication_set.add(item)
            self._cv.notify()

    def get(self) -> Optional[Any]:
        with self._cv:
            while not self._queue:
                self._cv.wait()
            return self._queue.popleft()

    def is_empty(self) -> bool:
        with self._cv:
            return len(self._queue) == 0

    def task_done(self) -> None:
        pass
