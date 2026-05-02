from sqlmodel import SQLModel, Field

PROJECT_ROLES = ["owner", "editor", "viewer"]


class ProyectoUsuarioCreate(SQLModel):
    id_usuario: int
    rol_proyecto: str = Field(default="viewer")


class ProyectoUsuarioEmailCreate(SQLModel):
    email: str
    rol_proyecto: str = Field(default="viewer")


class ProyectoUsuarioResponse(SQLModel):
    id_proyecto_usuario: int
    id_proyecto: int
    id_usuario: int
    rol_proyecto: str
    nombre_usuario: str | None = None
    email_usuario: str | None = None


class ProyectoUsuarioUpdate(SQLModel):
    rol_proyecto: str | None = None
