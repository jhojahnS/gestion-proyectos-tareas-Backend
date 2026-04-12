from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolResponse, RolUpdate
from app.db.session import get_session


class RolService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, rol_data: RolCreate) -> RolResponse:
        rol = Rol(**rol_data.model_dump())
        self.session.add(rol)
        self.session.commit()
        self.session.refresh(rol)
        return RolResponse(**rol.model_dump())

    def get_all(self):
        return self.session.exec(select(Rol)).all()

    def get_by_id(self, id: int):
        rol = self.session.get(Rol, id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol

    def update(self, id: int, rol_data: RolUpdate) -> Rol:
        rol = self.session.get(Rol, id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        rol_dict = rol_data.model_dump(exclude_unset=True)
        for key, value in rol_dict.items():
            setattr(rol, key, value)

        self.session.add(rol)
        self.session.commit()
        self.session.refresh(rol)
        return rol

    def delete(self, id: int):
        rol = self.session.get(Rol, id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        self.session.delete(rol)
        self.session.commit()
        return {"message": "Rol eliminado exitosamente"}
