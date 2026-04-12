from sqlmodel import SQLModel


class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    password: str
    id_rol: int


class UsuarioResponse(UsuarioCreate):
    id_usuario: int


class UsuarioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None
    password: str | None = None
    id_rol: int | None = None