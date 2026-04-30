from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.core.auth import is_global_admin
from app.models.tarea import Tarea
from app.models.proyecto_usuario import ProyectoUsuario
from app.schemas.tarea import TareaCreate, TareaResponse, TareaUpdate
from app.db.session import get_session


class TareaService:
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

    def _can_modify_task(self, project_id: int, user) -> bool:
        """
        Verifica si el usuario puede modificar tareas del proyecto.
        Admin, owner y editor pueden modificar.
        """
        if is_global_admin(user):
            return True

        rol = self._get_user_project_role(project_id, user.id_usuario)
        return rol in ["owner", "editor"] if rol else False

    def _can_view_task(self, project_id: int, user) -> bool:
        """
        Verifica si el usuario puede ver tareas del proyecto.
        Admin o miembros pueden ver.
        """
        if is_global_admin(user):
            return True

        rol = self._get_user_project_role(project_id, user.id_usuario)
        return rol is not None

    def create(
        self, tarea_data: TareaCreate, user
    ) -> TareaResponse:
        """
        Crea una tarea.
        Solo owner, editor o admin pueden crear tareas.
        """
        if not self._can_modify_task(tarea_data.id_proyecto, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para crear tareas en este proyecto",
            )

        tarea = Tarea(**tarea_data.model_dump())
        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)
        return TareaResponse(**tarea.model_dump())

    def get_all(self, user):
        """
        Lista tareas:
        - Admin global: todas las tareas
        - Usuario normal: tareas de proyectos donde es miembro
        """
        if is_global_admin(user):
            return self.session.exec(select(Tarea)).all()

        # Obtener proyectos donde el usuario es miembro
        proyectos_ids = self.session.exec(
            select(ProyectoUsuario.id_proyecto)
            .where(ProyectoUsuario.id_usuario == user.id_usuario)
        ).all()

        if not proyectos_ids:
            return []

        return self.session.exec(
            select(Tarea).where(Tarea.id_proyecto.in_(proyectos_ids))
        ).all()

    def get_by_id(self, id: int, user):
        """
        Obtiene una tarea por ID.
        Solo admin o miembros del proyecto pueden verla.
        """
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(
                status_code=404,
                detail="Tarea no encontrada"
            )

        if not self._can_view_task(tarea.id_proyecto, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver esta tarea",
            )

        return tarea

    def update(
        self, id: int, tarea_data: TareaUpdate, user
    ) -> Tarea:
        """
        Actualiza una tarea.
        Solo owner, editor o admin pueden editar.
        """
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(
                status_code=404,
                detail="Tarea no encontrada"
            )

        if not self._can_modify_task(tarea.id_proyecto, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para editar esta tarea",
            )

        tarea_dict = tarea_data.model_dump(exclude_unset=True)
        for key, value in tarea_dict.items():
            setattr(tarea, key, value)

        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)
        return tarea

    def delete(self, id: int, user):
        """
        Elimina una tarea.
        Solo owner, editor o admin pueden borrar.
        """
        tarea = self.session.get(Tarea, id)
        if not tarea:
            raise HTTPException(
                status_code=404,
                detail="Tarea no encontrada"
            )

        if not self._can_modify_task(tarea.id_proyecto, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para borrar esta tarea",
            )

        self.session.delete(tarea)
        self.session.commit()
        return {"message": "Tarea eliminada exitosamente"}
