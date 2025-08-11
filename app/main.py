from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import items
from .database import create_db_and_tables

app = FastAPI(
    title="Backend Scaffolding",
    description="A simple FastAPI backend with SQLModel and Alembic",
    version="0.1.0"
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
    """Create database tables on startup"""
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 