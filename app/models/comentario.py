from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.tarea import Tarea
    from app.models.usuario import Usuario


class Comentario(SQLModel, table=True):
    id_comentario: int | None = Field(default=None, primary_key=True)
    contenido: str
    fecha: datetime | None = None
    id_tarea: int = Field(foreign_key="tarea.id_tarea")
    id_usuario: int = Field(foreign_key="usuario.id_usuario")

    tarea: "Tarea" = Relationship(back_populates="comentarios")
    usuario: "Usuario" = Relationship(back_populates="comentarios")
