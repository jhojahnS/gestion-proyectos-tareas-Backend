from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from app.db.session import get_session


class ProyectoService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, proyecto_data: ProyectoCreate) -> ProyectoResponse:
        proyecto = Proyecto(**proyecto_data.model_dump())
        self.session.add(proyecto)
        self.session.commit()
        self.session.refresh(proyecto)
        return ProyectoResponse(**proyecto.model_dump())

    def get_all(self):
        return self.session.exec(select(Proyecto)).all()

    def get_by_id(self, id: int):
        proyecto = self.session.get(Proyecto, id)
        if not proyecto:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        return proyecto

    def update(self, id: int, proyecto_data: ProyectoUpdate) -> Proyecto:
        proyecto = self.session.get(Proyecto, id)
        if not proyecto:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        proyecto_dict = proyecto_data.model_dump(exclude_unset=True)
        for key, value in proyecto_dict.items():
            setattr(proyecto, key, value)

        self.session.add(proyecto)
        self.session.commit()
        self.session.refresh(proyecto)
        return proyecto

    def delete(self, id: int):
        proyecto = self.session.get(Proyecto, id)
        if not proyecto:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        self.session.delete(proyecto)
        self.session.commit()
        return {"message": "Proyecto eliminado exitosamente"}
