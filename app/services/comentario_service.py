from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import is_global_admin
from app.db.session import get_session
from app.models.comentario import Comentario
from app.models.proyecto_usuario import ProyectoUsuario
from app.models.tarea import Tarea
from app.schemas.comentario import (
    ComentarioCreate,
    ComentarioResponse,
    ComentarioUpdate,
)


class ComentarioService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_user_project_role(
        self, project_id: int, user_id: int
    ) -> str | None:
        """Obtiene el rol del usuario en el proyecto"""
        proyecto_usuario = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == project_id)
            .where(ProyectoUsuario.id_usuario == user_id)
        ).first()
        return (
            proyecto_usuario.rol_proyecto if proyecto_usuario else None
        )

    def _can_access_task(self, task_id: int, user) -> bool:
        """
        Verifica si el usuario puede acceder a la tarea.
        Admin o miembros del proyecto pueden acceder.
        """
        tarea = self.session.get(Tarea, task_id)
        if not tarea:
            return False

        if is_global_admin(user):
            return True

        rol = self._get_user_project_role(
            tarea.id_proyecto, user.id_usuario
        )
        return rol is not None

    def create(
        self,
        comentario_data: ComentarioCreate,
        user,
    ) -> ComentarioResponse:
        """
        Crea un comentario.
        Solo miembros del proyecto pueden comentar.
        """
        tarea = self.session.get(Tarea, comentario_data.id_tarea)
        if not tarea:
            raise HTTPException(
                status_code=404,
                detail="Tarea no encontrada",
            )

        if not self._can_access_task(comentario_data.id_tarea, user):
            raise HTTPException(
                status_code=403,
                detail=(
                    "No tienes permiso para comentar en esta tarea"
                ),
            )

        comentario = Comentario(**comentario_data.model_dump())
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return ComentarioResponse(**comentario.model_dump())

    def get_all(self, user):
        """
        Lista comentarios:
        - Admin global: todos los comentarios
        - Usuario normal: comentarios de proyectos donde es miembro
        """
        if is_global_admin(user):
            return self.session.exec(select(Comentario)).all()

        # Obtener proyectos donde el usuario es miembro
        proyectos_ids = self.session.exec(
            select(ProyectoUsuario.id_proyecto)
            .where(ProyectoUsuario.id_usuario == user.id_usuario)
        ).all()

        if not proyectos_ids:
            return []

        # Obtener comentarios de tareas de esos proyectos
        return self.session.exec(
            select(Comentario)
            .join(Tarea)
            .where(Tarea.id_proyecto.in_(proyectos_ids))
        ).all()

    def get_by_id(self, id: int, user):
        """
        Obtiene un comentario por ID.
        Solo admin o miembros del proyecto pueden verlo.
        """
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(
                status_code=404,
                detail="Comentario no encontrado",
            )

        if not self._can_access_task(comentario.id_tarea, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver este comentario",
            )

        return comentario

    def update(
        self,
        id: int,
        comentario_data: ComentarioUpdate,
        user,
    ) -> Comentario:
        """
        Actualiza un comentario.
        Solo el autor del comentario o admin pueden editar.
        """
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(
                status_code=404,
                detail="Comentario no encontrado",
            )

        # Verificar acceso a la tarea
        if not self._can_access_task(comentario.id_tarea, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para acceder a este comentario",
            )

        # Solo el autor o admin pueden editar
        if (
            not is_global_admin(user) and
            comentario.id_usuario != user.id_usuario
        ):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para editar este comentario",
            )

        comentario_dict = comentario_data.model_dump(exclude_unset=True)
        for key, value in comentario_dict.items():
            setattr(comentario, key, value)

        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def delete(self, id: int, user):
        """
        Elimina un comentario.
        Solo el autor del comentario o admin pueden borrar.
        """
        comentario = self.session.get(Comentario, id)
        if not comentario:
            raise HTTPException(
                status_code=404,
                detail="Comentario no encontrado",
            )

        # Verificar acceso a la tarea
        if not self._can_access_task(comentario.id_tarea, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para acceder a este comentario",
            )

        # Solo el autor o admin pueden borrar
        if (
            not is_global_admin(user) and
            comentario.id_usuario != user.id_usuario
        ):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para borrar este comentario",
            )

        self.session.delete(comentario)
        self.session.commit()
        return {"message": "Comentario eliminado exitosamente"}
