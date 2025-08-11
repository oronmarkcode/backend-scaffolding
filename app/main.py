from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import items
from app.database import create_test_db

app = FastAPI(
    title="Backend Scaffolding",
    description="A simple FastAPI backend with SQLModel and Alembic",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend Scaffolding is running!"}


@app.on_event("startup")
async def startup_event():
    """Create testdb database on startup"""
    create_test_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
