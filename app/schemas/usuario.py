from sqlmodel import SQLModel
from sqlmodel import SQLModel, Field


class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    password: str = Field(min_length=8, max_length=72)
    id_rol: int


class UsuarioResponse(SQLModel):
    id_usuario: int
    nombre: str
    email: str
    id_rol: int

class UsuarioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None
    password: str | None = Field(default=None,min_length=8,max_length=72)
    id_rol: int | None = None
