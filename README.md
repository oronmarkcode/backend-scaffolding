# Backend Scaffolding

A simple FastAPI backend template with SQLModel, Alembic, and PostgreSQL.

## Features

- FastAPI with automatic API documentation (Swagger UI at `/docs`)
- SQLModel for data modeling (not Pydantic BaseModel)
- Alembic for database migrations
- PostgreSQL database
- Simple CRUD operations for Items
- Health check endpoint at `/health`
- Docker Compose for PostgreSQL

## Project Structure

```
backend-scaffolding/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLModel models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py             # CRUD operations
│   └── api/
│       ├── __init__.py
│       └── items.py         # Items API routes
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial.py
├── docker-compose.yml       # PostgreSQL service
├── pyproject.toml           # Poetry dependencies
├── alembic.ini             # Alembic configuration
└── README.md
```

## Prerequisites

- Python 3.9+
- Poetry
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Quick Start

### 1. Install Dependencies

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Start PostgreSQL Database

```bash
# Start PostgreSQL in Docker
docker-compose up -d postgres

# Wait for database to be ready (check health status)
docker-compose ps
```

### 3. Run Database Migrations

```bash
# Run initial migration
poetry run alembic upgrade head
```

### 4. Start the FastAPI Server

```bash
# Start the server with auto-reload
poetry run start

# Or manually
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- `GET /health` - Server health status

### Items CRUD
- `GET /items/` - Get all items
- `POST /items/` - Create a new item
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item (soft delete)

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Models

The project includes a simple `Item` model with:
- `id`: UUID primary key
- `name`: String (required)
- `description`: Optional string
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `deleted_at`: Optional timestamp (for soft deletes)

## Development

### Adding New Models

1. Add the model to `app/models.py`
2. Create a new Alembic migration:
   ```bash
   alembic revision --autogenerate -m "Add new model"
   ```
3. Apply the migration:
   ```bash
   poetry run alembic upgrade head
   ```

### Running Tests

```bash
poetry run pytest
```

### Database Reset

```bash
# Stop the database
docker-compose down

# Remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d postgres
poetry run alembic upgrade head
```

## Environment Variables

Copy `env.example` to `.env` and modify as needed:

```bash
cp env.example .env
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `docker-compose ps`
- Check database logs: `docker-compose logs postgres`
- Verify connection string in `app/config.py`

### Migration Issues
- Check Alembic version: `poetry run alembic current`
- Reset migrations: `poetry run alembic downgrade base` then `poetry run alembic upgrade head`

### Port Conflicts
- Change ports in `docker-compose.yml` and `app/config.py` if needed
- Default: FastAPI on 8000, PostgreSQL on 5432

## License

This is a template project. Modify as needed for your use case.