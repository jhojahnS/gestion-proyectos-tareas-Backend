from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioCreate, ComentarioResponse, ComentarioUpdate
from app.db.session import get_session


class ComentarioService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, comentario_data: ComentarioCreate) -> ComentarioResponse:
        comentario = Comentario(**comentario_data.model_dump())
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return ComentarioResponse(**comentario.model_dump())

    def get_all(self):
        return self.session.exec(select(Comentario)).all()

    def get_by_id(self, id: int):
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return comentario

    def update(self, id: int, comentario_data: ComentarioUpdate) -> Comentario:
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")

        comentario_dict = comentario_data.model_dump(exclude_unset=True)
        for key, value in comentario_dict.items():
            setattr(comentario, key, value)

        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def delete(self, id: int):
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")

        self.session.delete(comentario)
        self.session.commit()
        return {"message": "Comentario eliminado exitosamente"}