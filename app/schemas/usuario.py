from sqlmodel import SQLModel, Field

from app.core.security import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH


class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
    id_rol: int


class UsuarioResponse(SQLModel):
    id_usuario: int
    nombre: str
    email: str
    id_rol: int


class UsuarioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None
    password: str | None = Field(
        default=None,
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
    id_rol: int | None = None
