from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "gestion-proyectos-tareas-backend"
    database_url: str = "sqlite:///./database.db"

    class Config:
        env_file = ".env"


settings = Settings()
