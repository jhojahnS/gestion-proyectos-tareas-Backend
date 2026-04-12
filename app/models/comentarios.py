from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Comentario(SQLModel, table=True):
    id_comentario: int | None = Field(default=None, primary_key=True)
    contenido: str
    fecha: datetime | None = None
    id_tarea: int = Field(foreign_key="tarea.id_tarea")
    id_usuario: int = Field(foreign_key="usuario.id_usuario")

    tarea: "Tarea" = Relationship(back_populates="comentarios")
    usuario: "Usuario" = Relationship(back_populates="comentarios")