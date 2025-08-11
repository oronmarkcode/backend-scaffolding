from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Iterator, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str | None = None
    content: str


class AIConfig(ABC):
    temperature: float = 0.7
    max_tokens: int = 512
    model_id: str


class EmbeddingConfig(ABC):
    model: Optional[str] = None
    dimensions: Optional[int] = None


class AIProvider(ABC):
    def __init__(self, ai_config: AIConfig, embedding_config: EmbeddingConfig):
        self.ai_config = ai_config
        self.embedding_config = embedding_config

    @abstractmethod
    def invoke(self, messages: List[Message]) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream(self, messages: List[Message]) -> Iterator[str]:
        raise NotImplementedError

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError
