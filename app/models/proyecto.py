from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Proyecto(SQLModel, table=True):
    id_proyecto: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
    fecha_creacion: date | None = None

    tareas: list["Tarea"] = Relationship(back_populates="proyecto", cascade_delete=True)
