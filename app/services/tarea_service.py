from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.tarea import Tarea
from app.schemas.tarea import TareaCreate, TareaResponse, TareaUpdate
from app.db.session import get_session


class TareaService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, tarea_data: TareaCreate) -> TareaResponse:
        tarea = Tarea(**tarea_data.model_dump())
        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)
        return TareaResponse(**tarea.model_dump())

    def get_all(self):
        return self.session.exec(select(Tarea)).all()

    def get_by_id(self, id: int):
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return tarea

    def update(self, id: int, tarea_data: TareaUpdate) -> Tarea:
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        tarea_dict = tarea_data.model_dump(exclude_unset=True)
        for key, value in tarea_dict.items():
            setattr(tarea, key, value)

        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)
        return tarea

    def delete(self, id: int):
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        self.session.delete(tarea)
        self.session.commit()
        return {"message": "Tarea eliminada exitosamente"}
