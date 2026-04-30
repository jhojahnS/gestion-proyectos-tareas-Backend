from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.proyecto import Proyecto
    from app.models.usuario import Usuario


class ProyectoUsuario(SQLModel, table=True):
    id_proyecto_usuario: int | None = Field(default=None, primary_key=True)
    id_proyecto: int = Field(foreign_key="proyecto.id_proyecto")
    id_usuario: int = Field(foreign_key="usuario.id_usuario")
    rol_proyecto: str = Field(default="viewer")

    proyecto: "Proyecto" = Relationship(back_populates="miembros")
    usuario: "Usuario" = Relationship(back_populates="proyectos_miembro")
