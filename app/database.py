import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

# Create engine without auto-creating tables
engine = create_engine(settings.database_url, echo=settings.debug)


def create_test_db():
    """Create testdb database if it doesn't exist"""
    try:
        # Connect to default postgres database to create new database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="postgres",  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='testdb'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE testdb")
            print("Database 'testdb' created successfully")
        else:
            print("Database 'testdb' already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")


def get_session():
    with Session(engine) as session:
        yield session
