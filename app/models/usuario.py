from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship


class Usuario(SQLModel, table=True):
    id_usuario: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str
    password: str
    id_rol: int = Field(foreign_key="rol.id_rol")

    rol: "Rol" = Relationship(back_populates="usuarios")
    tareas_asignadas: list["Tarea"] = Relationship(
        back_populates="usuario_asignado"
    )
    comentarios: list["Comentario"] = Relationship(
        back_populates="usuario"
    )
