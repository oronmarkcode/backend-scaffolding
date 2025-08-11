from typing import Optional
from sqlmodel import SQLModel


class ItemCreate(SQLModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ItemResponse(SQLModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str 