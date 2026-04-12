from sqlmodel import SQLModel
from datetime import datetime


class ComentarioCreate(SQLModel):
    contenido: str
    fecha: datetime | None = None
    id_tarea: int
    id_usuario: int


class ComentarioResponse(ComentarioCreate):
    id_comentario: int


class ComentarioUpdate(SQLModel):
    contenido: str | None = None
    fecha: datetime | None = None
    id_tarea: int | None = None
    id_usuario: int | None = None