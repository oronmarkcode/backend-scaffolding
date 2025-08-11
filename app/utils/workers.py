from __future__ import annotations

import threading
from typing import Any, Callable, List

_STOP = object()


class WorkerGroup:
    def __init__(
        self,
        queue,
        worker: Callable[[Any], None],
        *,
        threads: int = 1,
        name: str = "Worker",
    ) -> None:
        self.queue = queue
        self.worker = worker
        self.threads = threads
        self.name = name
        self._threads: List[threading.Thread] = []
        self._started = False

    def start(self) -> "WorkerGroup":
        if self._started:
            return self
        self._started = True
        for i in range(self.threads):
            t = threading.Thread(
                target=self._loop, name=f"{self.name}-{i+1}", daemon=True
            )
            t.start()
            self._threads.append(t)
        return self

    def _loop(self) -> None:
        while True:
            item = self.queue.get()
            try:
                if item is _STOP:
                    return
                self.worker(item)
            finally:
                self.queue.task_done()

    def stop(self) -> None:
        for _ in range(len(self._threads)):
            self.queue.put(_STOP)

    def join(self) -> None:
        for t in self._threads:
            t.join()
