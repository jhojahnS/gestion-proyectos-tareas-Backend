from sqlmodel import SQLModel


class TareaCreate(SQLModel):
    titulo: str
    descripcion: str | None = None
    id_proyecto: int
    estado: str = "Pendiente"  # Estado por defecto
    id_usuario_asignado: int | None = None


class TareaResponse(SQLModel):
    id_tarea: int
    titulo: str
    descripcion: str | None
    estado: str
    id_proyecto: int
    nombre_proyecto: str | None = None  # Enriquecido para frontend
    id_usuario_asignado: int | None = None
    nombre_usuario_asignado: str | None = None  # Enriquecido para frontend


class TareaUpdate(SQLModel):
    titulo: str | None = None
    descripcion: str | None = None
    estado: str | None = None
    id_usuario_asignado: int | None = None
    # id_proyecto NO es editable - se omite intencionalmente
