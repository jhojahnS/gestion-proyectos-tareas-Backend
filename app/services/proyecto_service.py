from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import is_global_admin
from app.db.session import get_session
from app.models.proyecto import Proyecto
from app.models.proyecto_usuario import ProyectoUsuario
from app.models.usuario import Usuario
from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoResponse,
    ProyectoUpdate,
)
from app.schemas.proyecto_usuario import (
    PROJECT_ROLES,
    ProyectoUsuarioCreate,
    ProyectoUsuarioResponse,
)


class ProyectoService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(
            self,
            proyecto_data: ProyectoCreate,
            user_id: int,
    ) -> ProyectoResponse:
        proyecto = Proyecto(
            **proyecto_data.model_dump(),
            creado_por_id=user_id,
        )

        self.session.add(proyecto)
        self.session.commit()
        self.session.refresh(proyecto)

        miembro = ProyectoUsuario(
            id_proyecto=proyecto.id_proyecto,
            id_usuario=user_id,
            rol_proyecto="owner",
        )

        self.session.add(miembro)
        self.session.commit()

        return ProyectoResponse(
            id_proyecto=proyecto.id_proyecto,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            fecha_creacion=proyecto.fecha_creacion,
            creado_por_id=proyecto.creado_por_id,
        )

    def get_all(self):
        """Devuelve todos los proyectos (solo para admin global)"""
        return self.session.exec(select(Proyecto)).all()

    def get_by_user(self, user_id: int):
        """Devuelve solo los proyectos donde el usuario es miembro"""
        statement = (
            select(Proyecto)
            .join(ProyectoUsuario)
            .where(ProyectoUsuario.id_usuario == user_id)
        )
        return self.session.exec(statement).all()

    def get_by_id(self, id: int):
        """Devuelve proyecto por ID o 404"""
        proyecto = self.session.get(Proyecto, id)
        if not proyecto:
            raise HTTPException(
                status_code=404,
                detail="Proyecto no encontrado",
            )
        return proyecto

    def get_by_id_for_user(self, id: int, user):
        """
        Devuelve proyecto por ID verificando permisos:
        - Admin global: puede ver cualquier proyecto
        - Usuario normal: solo si es miembro
        """
        proyecto = self.get_by_id(id)

        if is_global_admin(user):
            return proyecto

        if not self.is_project_member(id, user.id_usuario):
            raise HTTPException(
                status_code=403,
                detail="No autorizado para ver este proyecto",
            )

        return proyecto

    def update(
        self,
        id: int,
        proyecto_data: ProyectoUpdate,
        user,
    ) -> Proyecto:
        """
        Actualiza un proyecto.
        Solo admin global, owner o editor pueden editar.
        """
        proyecto = self.get_by_id(id)

        if not self.has_project_permission(
            id, user, ["owner", "editor"]
        ):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para editar este proyecto",
            )

        proyecto_dict = proyecto_data.model_dump(exclude_unset=True)
        for key, value in proyecto_dict.items():
            setattr(proyecto, key, value)

        self.session.add(proyecto)
        self.session.commit()
        self.session.refresh(proyecto)
        return proyecto

    def delete(self, id: int, user):
        """
        Elimina un proyecto.
        Solo admin global u owner pueden borrar.
        """
        proyecto = self.get_by_id(id)

        if not self.has_project_permission(id, user, ["owner"]):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para borrar este proyecto",
            )

        self.session.delete(proyecto)
        self.session.commit()
        return {"message": "Proyecto eliminado exitosamente"}

    def add_member(
        self,
        project_id: int,
        member_data: ProyectoUsuarioCreate,
        user,
    ) -> ProyectoUsuarioResponse:
        """
        Añade un miembro al proyecto.
        Solo admin global u owner pueden añadir miembros.
        """
        # Verificar que el proyecto existe
        self.get_by_id(project_id)

        # Verificar permisos
        if not self.has_project_permission(project_id, user, ["owner"]):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para añadir miembros",
            )

        # Verificar que el usuario a añadir existe
        usuario_a_añadir = self.session.get(
            Usuario, member_data.id_usuario
        )
        if not usuario_a_añadir:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )

        # Verificar que no esté ya añadido
        existing = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(ProyectoUsuario.id_usuario == member_data.id_usuario)
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya es miembro del proyecto",
            )

        # Validar rol_proyecto
        if member_data.rol_proyecto not in PROJECT_ROLES:
            raise HTTPException(
                status_code=400,
                detail="Rol inválido. Debe ser: owner, editor o viewer",
            )

        # Crear ProyectoUsuario
        proyecto_usuario = ProyectoUsuario(
            id_proyecto=project_id,
            id_usuario=member_data.id_usuario,
            rol_proyecto=member_data.rol_proyecto,
        )
        self.session.add(proyecto_usuario)
        self.session.commit()
        self.session.refresh(proyecto_usuario)

        return ProyectoUsuarioResponse(
            id_proyecto_usuario=proyecto_usuario.id_proyecto_usuario,
            id_proyecto=proyecto_usuario.id_proyecto,
            id_usuario=proyecto_usuario.id_usuario,
            rol_proyecto=proyecto_usuario.rol_proyecto,
        )

    def add_member_by_email(
        self,
        project_id: int,
        email: str,
        rol_proyecto: str,
        user,
    ) -> ProyectoUsuarioResponse:
        """
        Añade un miembro al proyecto buscándolo por email.
        Solo admin global u owner pueden añadir miembros.
        """
        # Verificar que el proyecto existe
        self.get_by_id(project_id)

        # Verificar permisos
        if not self.has_project_permission(project_id, user, ["owner"]):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para añadir miembros",
            )

        # Validar rol_proyecto
        if rol_proyecto not in PROJECT_ROLES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Rol inválido. Debe ser: owner, editor o viewer"
                ),
            )

        # Buscar usuario por email
        usuario_a_añadir = self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()

        if not usuario_a_añadir:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )

        # Verificar que no esté ya añadido
        existing = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(
                ProyectoUsuario.id_usuario
                == usuario_a_añadir.id_usuario
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya es miembro del proyecto",
            )

        # Crear ProyectoUsuario
        proyecto_usuario = ProyectoUsuario(
            id_proyecto=project_id,
            id_usuario=usuario_a_añadir.id_usuario,
            rol_proyecto=rol_proyecto,
        )
        self.session.add(proyecto_usuario)
        self.session.commit()
        self.session.refresh(proyecto_usuario)

        return ProyectoUsuarioResponse(
            id_proyecto_usuario=proyecto_usuario.id_proyecto_usuario,
            id_proyecto=proyecto_usuario.id_proyecto,
            id_usuario=proyecto_usuario.id_usuario,
            rol_proyecto=proyecto_usuario.rol_proyecto,
        )

    def remove_member(
        self,
        project_id: int,
        user_id_to_remove: int,
        user,
    ):
        """
        Elimina un miembro del proyecto.
        Solo admin global u owner pueden quitar miembros.
        No permitir que un owner se quite a sí mismo si es el único owner.
        """
        # Verificar que el proyecto existe
        self.get_by_id(project_id)

        # Verificar permisos
        if not self.has_project_permission(project_id, user, ["owner"]):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para quitar miembros",
            )

        # Buscar la relación
        proyecto_usuario = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(ProyectoUsuario.id_usuario == user_id_to_remove)
        ).first()

        if not proyecto_usuario:
            raise HTTPException(
                status_code=404,
                detail="El usuario no es miembro del proyecto",
            )

        # Verificar que no sea el último owner
        if proyecto_usuario.rol_proyecto == "owner":
            owners_count = self.session.exec(
                select(ProyectoUsuario)
                .where(ProyectoUsuario.id_proyecto == project_id)
                .where(ProyectoUsuario.rol_proyecto == "owner")
            ).all()

            if len(owners_count) <= 1:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No se puede eliminar el último owner del proyecto"
                    ),
                )

        self.session.delete(proyecto_usuario)
        self.session.commit()
        return {"message": "Miembro eliminado exitosamente"}

    def update_member_role(
        self,
        project_id: int,
        member_id: int,
        rol_proyecto: str,
        user,
    ) -> ProyectoUsuarioResponse:
        """
        Cambia el rol de un miembro del proyecto.
        Solo admin global u owner pueden cambiar roles.
        """
        # Verificar que el proyecto existe
        self.get_by_id(project_id)

        # Verificar permisos
        if not self.has_project_permission(project_id, user, ["owner"]):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para cambiar roles",
            )

        # Validar rol_proyecto
        if rol_proyecto not in PROJECT_ROLES:
            raise HTTPException(
                status_code=400,
                detail="Rol inválido. Debe ser: owner, editor o viewer",
            )

        # Buscar el miembro
        proyecto_usuario = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(ProyectoUsuario.id_usuario == member_id)
        ).first()

        if not proyecto_usuario:
            raise HTTPException(
                status_code=404,
                detail="El usuario no es miembro del proyecto",
            )

        # Si se intenta cambiar de owner a otro rol, verificar
        # que no sea el último owner
        if (
            proyecto_usuario.rol_proyecto == "owner" and
            rol_proyecto != "owner"
        ):
            owners_count = self.session.exec(
                select(ProyectoUsuario)
                .where(ProyectoUsuario.id_proyecto == project_id)
                .where(ProyectoUsuario.rol_proyecto == "owner")
            ).all()

            if len(owners_count) <= 1:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No se puede cambiar el rol del único owner "
                        "del proyecto"
                    ),
                )

        proyecto_usuario.rol_proyecto = rol_proyecto
        self.session.add(proyecto_usuario)
        self.session.commit()
        self.session.refresh(proyecto_usuario)

        return ProyectoUsuarioResponse(
            id_proyecto_usuario=proyecto_usuario.id_proyecto_usuario,
            id_proyecto=proyecto_usuario.id_proyecto,
            id_usuario=proyecto_usuario.id_usuario,
            rol_proyecto=proyecto_usuario.rol_proyecto,
        )

    def get_user_project_role(
        self, project_id: int, user_id: int
    ) -> str | None:
        """Devuelve el rol del usuario en el proyecto o None"""
        proyecto_usuario = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(ProyectoUsuario.id_usuario == user_id)
        ).first()

        return (
            proyecto_usuario.rol_proyecto if proyecto_usuario else None
        )

    def is_project_member(self, project_id: int, user_id: int) -> bool:
        """Devuelve True si el usuario es miembro del proyecto"""
        return self.get_user_project_role(project_id, user_id) is not None

    def has_project_permission(
        self,
        project_id: int,
        user,
        allowed_roles: list[str]
    ) -> bool:
        """
        Verifica si el usuario tiene permiso en el proyecto.
        Admin global siempre tiene permiso.
        """
        if is_global_admin(user):
            return True

        rol = self.get_user_project_role(project_id, user.id_usuario)
        return rol in allowed_roles if rol else False

    def get_project_members(
        self, project_id: int, user
    ) -> list[ProyectoUsuarioResponse]:
        """
        Devuelve la lista de miembros del proyecto.
        Admin o miembros pueden ver la lista.
        """
        # Verificar que el proyecto existe
        self.get_by_id(project_id)

        # Verificar permisos
        if not is_global_admin(user) and not self.is_project_member(
            project_id, user.id_usuario
        ):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver los miembros",
            )

        miembros = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
        ).all()

        return [
            ProyectoUsuarioResponse(
                id_proyecto_usuario=m.id_proyecto_usuario,
                id_proyecto=m.id_proyecto,
                id_usuario=m.id_usuario,
                rol_proyecto=m.rol_proyecto,
            )
            for m in miembros
        ]
