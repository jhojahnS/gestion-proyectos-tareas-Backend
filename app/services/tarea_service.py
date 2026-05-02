from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.core.auth import is_global_admin
from app.models.tarea import Tarea
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.models.proyecto_usuario import ProyectoUsuario
from app.schemas.tarea import TareaCreate, TareaResponse, TareaUpdate
from app.db.session import get_session


class TareaService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _build_tarea_response(self, tarea: Tarea) -> TareaResponse:
        """
        Construye una respuesta enriquecida con nombres de proyecto y usuario.
        """
        # Obtener proyecto
        proyecto = self.session.get(Proyecto, tarea.id_proyecto)
        nombre_proyecto = proyecto.nombre if proyecto else None

        # Obtener usuario asignado si existe
        nombre_usuario_asignado = None
        if tarea.id_usuario_asignado:
            usuario = self.session.get(Usuario, tarea.id_usuario_asignado)
            nombre_usuario_asignado = usuario.nombre if usuario else None

        return TareaResponse(
            id_tarea=tarea.id_tarea,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            estado=tarea.estado,
            id_proyecto=tarea.id_proyecto,
            nombre_proyecto=nombre_proyecto,
            id_usuario_asignado=tarea.id_usuario_asignado,
            nombre_usuario_asignado=nombre_usuario_asignado,
        )

    def _validate_user_belongs_to_project(
        self, id_proyecto: int, id_usuario: int
    ) -> bool:
        """
        Valida que un usuario pertenezca al proyecto.
        """
        proyecto_usuario = self.session.exec(
            select(ProyectoUsuario)
            .where(ProyectoUsuario.id_proyecto == id_proyecto)
            .where(ProyectoUsuario.id_usuario == id_usuario)
        ).first()
        return proyecto_usuario is not None

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
        El estado por defecto es "Pendiente".
        El id_usuario_asignado es None por defecto.
        """
        # Verificar que el proyecto existe
        proyecto = self.session.get(Proyecto, tarea_data.id_proyecto)
        if not proyecto:
            raise HTTPException(
                status_code=404,
                detail="Proyecto no encontrado"
            )

        # Verificar permisos del usuario creador
        if not self._can_modify_task(tarea_data.id_proyecto, user):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para crear tareas en este proyecto",
            )

        # Validar usuario asignado si se proporciona
        if tarea_data.id_usuario_asignado is not None:
            if not self._validate_user_belongs_to_project(
                tarea_data.id_proyecto,
                tarea_data.id_usuario_asignado
            ):
                raise HTTPException(
                    status_code=400,
                    detail="El usuario asignado no pertenece a este proyecto"
                )

        tarea = Tarea(**tarea_data.model_dump())
        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)

        return self._build_tarea_response(tarea)

    def get_all(self, user) -> list[TareaResponse]:
        """
        Lista tareas:
        - Admin global: todas las tareas
        - Usuario normal: tareas de proyectos donde es miembro
        """
        if is_global_admin(user):
            tareas = self.session.exec(select(Tarea)).all()
        else:
            # Obtener proyectos donde el usuario es miembro
            proyectos_ids = self.session.exec(
                select(ProyectoUsuario.id_proyecto)
                .where(ProyectoUsuario.id_usuario == user.id_usuario)
            ).all()

            if not proyectos_ids:
                return []

            tareas = self.session.exec(
                select(Tarea).where(Tarea.id_proyecto.in_(proyectos_ids))
            ).all()

        # Devolver respuestas enriquecidas
        return [self._build_tarea_response(tarea) for tarea in tareas]

    def get_by_id(self, id: int, user) -> TareaResponse:
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

        return self._build_tarea_response(tarea)

    def update(
        self, id: int, tarea_data: TareaUpdate, user
    ) -> TareaResponse:
        """
        Actualiza una tarea.
        Solo owner, editor o admin pueden editar.
        No se permite cambiar el proyecto asociado.
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

        # Validar usuario asignado si se proporciona
        tarea_dict = tarea_data.model_dump(exclude_unset=True)
        if "id_usuario_asignado" in tarea_dict:
            id_usuario = tarea_dict["id_usuario_asignado"]
            if id_usuario is not None:  # Si se asigna un usuario (no None)
                if not self._validate_user_belongs_to_project(
                    tarea.id_proyecto,
                    id_usuario
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "El usuario asignado no pertenece a "
                            "este proyecto"
                        )
                    )

        # Actualizar solo los campos permitidos
        # (id_proyecto no está en TareaUpdate)
        for key, value in tarea_dict.items():
            setattr(tarea, key, value)

        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)

        return self._build_tarea_response(tarea)

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
