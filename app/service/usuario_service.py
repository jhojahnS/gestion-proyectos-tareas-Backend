from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.db.session import get_session


class UsuarioService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, usuario_data: UsuarioCreate) -> UsuarioResponse:
        usuario = Usuario(**usuario_data.model_dump())
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return UsuarioResponse(**usuario.model_dump())

    def get_all(self):
        return self.session.exec(select(Usuario)).all()

    def get_by_id(self, id: int):
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    def update(self, id: int, usuario_data: UsuarioUpdate) -> Usuario:
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario_dict = usuario_data.model_dump(exclude_unset=True)
        for key, value in usuario_dict.items():
            setattr(usuario, key, value)

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def delete(self, id: int):
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        self.session.delete(usuario)
        self.session.commit()
        return {"message": "Usuario eliminado exitosamente"}