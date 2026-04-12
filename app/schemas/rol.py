from sqlmodel import SQLModel


class RolCreate(SQLModel):
    nombre: str


class RolResponse(RolCreate):
    id_rol: int


class RolUpdate(SQLModel):
    nombre: str | None = None