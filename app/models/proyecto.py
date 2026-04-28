from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.tarea import Tarea


class Proyecto(SQLModel, table=True):
    id_proyecto: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
    fecha_creacion: date | None = None

    tareas: list["Tarea"] = Relationship(
        back_populates="proyecto",
        cascade_delete=True,
    )

    usuario_id: int = Field(foreign_key="usuario.id_usuario")
