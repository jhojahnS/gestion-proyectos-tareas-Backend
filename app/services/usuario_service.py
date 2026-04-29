from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.core.security import hash_password

from app.db.session import get_session
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)


class UsuarioService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(
        self,
        usuario_data: UsuarioCreate,
    ) -> UsuarioResponse:
        role = self.session.get(Rol, usuario_data.id_rol)
        if not role:
            raise HTTPException(
                status_code=400,
                detail=f"El rol con id {usuario_data.id_rol} no existe",
            )

        usuario_dict = usuario_data.model_dump()
        usuario_dict["hashed_password"] = (
            hash_password(usuario_dict.pop("password"))
        )
        usuario = Usuario(**usuario_dict)
        self.session.add(usuario)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail=(
                    "No se pudo crear el usuario por conflicto de "
                    "integridad"
                ),
            )

        self.session.refresh(usuario)
        return UsuarioResponse(**usuario.model_dump())

    def get_all(self):
        return self.session.exec(select(Usuario)).all()

    def get_by_id(self, id: int):
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )
        return usuario

    def update(
        self,
        id: int,
        usuario_data: UsuarioUpdate,
    ) -> Usuario:
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )

        usuario_dict = usuario_data.model_dump(exclude_unset=True)

        if "id_rol" in usuario_dict and usuario_dict["id_rol"] is not None:
            role = self.session.get(Rol, usuario_dict["id_rol"])
            if not role:
                raise HTTPException(
                    status_code=400,
                    detail=f"El rol con id {usuario_dict['id_rol']} no existe",
                )

        if "password" in usuario_dict and usuario_dict["password"] is not None:
            usuario_dict["hashed_password"] = hash_password(
                usuario_dict.pop("password")
            )

        for key, value in usuario_dict.items():
            setattr(usuario, key, value)

        self.session.add(usuario)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail=(
                    "No se pudo actualizar el usuario por conflicto de "
                    "integridad"
                ),
            )

        self.session.refresh(usuario)
        return usuario

    def delete(self, id: int):
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )

        self.session.delete(usuario)
        self.session.commit()
        return {"message": "Usuario eliminado exitosamente"}

    def get_by_email(self, email: str):
        return self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()
