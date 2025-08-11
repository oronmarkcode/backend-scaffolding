from abc import ABC, abstractmethod
from collections import deque
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


class InMemoryQueue(Queue):
    def __init__(self) -> None:
        self._queue = deque()
        self._cv = Condition()

    def put(self, item: Any) -> None:
        with self._cv:
            self._queue.append(item)
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
