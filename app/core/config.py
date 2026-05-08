import os
from pydantic_settings import BaseSettings


def _build_database_url() -> str:
    """
    Construye la URL de conexión a PostgreSQL desde variables de entorno.
    Prioriza DATABASE_URL si existe, sino construye desde componentes.
    Permite despliegue en Docker/EC2 con Amazon RDS.
    """
    # Opción 1: Usar DATABASE_URL directamente si está definida
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Opción 2: Construir desde componentes individuales
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "gestion")
    db_user = os.getenv("DB_USER", "admin")
    db_password = os.getenv("DB_PASSWORD")

    # Validar que DB_PASSWORD esté definida (requerida para producción)
    if not db_password:
        # En desarrollo local, usar valor por defecto
        if db_host == "localhost":
            db_password = "admin"
        else:
            raise RuntimeError(
                "DB_PASSWORD environment variable is required. "
                "Please set DATABASE_URL or DB_PASSWORD in environment."
            )

    # Construir URL en formato PostgreSQL con psycopg2
    return (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


class Settings(BaseSettings):
    # Configuración de base de datos desde variables de entorno
    # Se construye automáticamente al importar
    database_url: str = _build_database_url()
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
