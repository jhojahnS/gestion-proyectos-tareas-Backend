from sqlmodel import SQLModel
from datetime import date


class ProyectoCreate(SQLModel):
    nombre: str
    descripcion: str | None = None
    fecha_creacion: date | None = None


class ProyectoResponse(ProyectoCreate):
    id_proyecto: int
    creado_por_id: int


class ProyectoUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    fecha_creacion: date | None = None
