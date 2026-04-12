from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.comentario import Comentario
    from app.models.proyecto import Proyecto
    from app.models.usuario import Usuario


class Tarea(SQLModel, table=True):
    id_tarea: int | None = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str | None = None
    estado: str
    id_proyecto: int = Field(foreign_key="proyecto.id_proyecto")
    id_usuario_asignado: int | None = Field(
        default=None,
        foreign_key="usuario.id_usuario",
    )

    proyecto: "Proyecto" = Relationship(
        back_populates="tareas",
    )
    usuario_asignado: "Usuario" = Relationship(
        back_populates="tareas_asignadas",
    )
    comentarios: list["Comentario"] = Relationship(
        back_populates="tarea",
        cascade_delete=True,
    )
