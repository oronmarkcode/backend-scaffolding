from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Backend Scaffolding"
    debug: bool = True
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/backend_scaffolding"
    
    class Config:
        env_file = ".env"


settings = Settings() 