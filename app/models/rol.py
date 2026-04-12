from sqlmodel import SQLModel, Field, Relationship

class Rol(SQLModel, table=True):
    id_rol: int | None = Field(default=None, primary_key=True)
    nombre: str

    usuarios: list["Usuario"] = Relationship(back_populates="rol")