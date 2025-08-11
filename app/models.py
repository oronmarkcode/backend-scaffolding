import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)


class Item(Base, TimestampMixin, table=True):
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(max_length=500, nullable=True)
