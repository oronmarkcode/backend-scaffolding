import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class ItemCreate(SQLModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ItemResponse(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
