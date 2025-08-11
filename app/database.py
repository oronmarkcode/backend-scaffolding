import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

# Create engine without auto-creating tables
engine = create_engine(settings.database_url, echo=settings.debug)


def get_session():
    with Session(engine) as session:
        yield session
