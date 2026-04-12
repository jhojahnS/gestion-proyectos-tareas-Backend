from sqlmodel import SQLModel


class TareaCreate(SQLModel):
    titulo: str
    descripcion: str | None = None
    estado: str
    id_proyecto: int
    id_usuario_asignado: int | None = None


class TareaResponse(TareaCreate):
    id_tarea: int


class TareaUpdate(SQLModel):
    titulo: str | None = None
    descripcion: str | None = None
    estado: str | None = None
    id_proyecto: int | None = None
    id_usuario_asignado: int | None = None

