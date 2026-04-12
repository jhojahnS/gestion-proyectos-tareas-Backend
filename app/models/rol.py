from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Rol(SQLModel, table=True):
    id_rol: int | None = Field(default=None, primary_key=True)
    nombre: str

    usuarios: list["Usuario"] = Relationship(
        back_populates="rol",
    )
