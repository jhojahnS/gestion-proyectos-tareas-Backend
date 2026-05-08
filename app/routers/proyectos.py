from fastapi import APIRouter, Depends
from app.core.auth import get_current_user, is_global_admin

from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoResponse,
    ProyectoUpdate,
)
from app.schemas.proyecto_usuario import (
    ProyectoUsuarioCreate,
    ProyectoUsuarioEmailCreate,
    ProyectoUsuarioResponse,
    ProyectoUsuarioUpdate,
)
from app.services.proyecto_service import ProyectoService

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProyectoResponse)
async def create_proyecto(
    proyecto: ProyectoCreate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """Crea un proyecto y añade al usuario autenticado como owner"""
    return service.create(proyecto, user.id_usuario)


@router.get("/")
def read_proyectos(
    user=Depends(get_current_user),
    service: ProyectoService = Depends()
):
    """
    Lista proyectos:
    - Admin global: ve todos los proyectos
    - Usuario normal: ve solo proyectos donde es miembro
    """
    if is_global_admin(user):
        return service.get_all()
    return service.get_by_user(user.id_usuario)


@router.get("/{id}", response_model=ProyectoResponse)
async def read_proyecto(
    id: int,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Obtiene un proyecto por ID.
    Solo admin global o miembros pueden verlo.
    """
    return service.get_by_id_for_user(id, user)


@router.patch("/{id}", response_model=ProyectoResponse)
async def update_proyecto(
    id: int,
    proyecto_data: ProyectoUpdate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Actualiza un proyecto.
    Solo admin global, owner o editor pueden editar.
    """
    return service.update(id, proyecto_data, user)


@router.delete("/{id}", response_model=dict)
async def delete_proyecto(
    id: int,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Elimina un proyecto.
    Solo admin global u owner pueden borrar.
    """
    return service.delete(id, user)


@router.get("/{id}/miembros", response_model=list[ProyectoUsuarioResponse])
async def get_project_members(
    id: int,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Lista los miembros de un proyecto.
    Admin global o miembros del proyecto pueden ver la lista.
    """
    return service.get_project_members(id, user)


@router.post("/{id}/miembros", response_model=ProyectoUsuarioResponse)
async def add_project_member(
    id: int,
    member_data: ProyectoUsuarioCreate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Añade un miembro al proyecto.
    Solo admin global u owner pueden añadir miembros.
    """
    return service.add_member(id, member_data, user)


@router.post(
    "/{id}/miembros/email",
    response_model=ProyectoUsuarioResponse
)
async def add_project_member_by_email(
    id: int,
    member_data: ProyectoUsuarioEmailCreate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Añade un miembro al proyecto buscándolo por email.
    Solo admin global u owner pueden añadir miembros.
    """
    return service.add_member_by_email(
        id, member_data.email, member_data.rol_proyecto, user
    )


@router.patch(
    "/{id}/miembros/{id_usuario}",
    response_model=ProyectoUsuarioResponse
)
async def update_member_role(
    id: int,
    id_usuario: int,
    member_data: ProyectoUsuarioUpdate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Cambia el rol de un miembro del proyecto.
    Solo admin global u owner pueden cambiar roles.
    """
    if member_data.rol_proyecto is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="rol_proyecto es requerido"
        )
    return service.update_member_role(
        id, id_usuario, member_data.rol_proyecto, user
    )


@router.delete("/{id}/miembros/{id_usuario}", response_model=dict)
async def remove_member(
    id: int,
    id_usuario: int,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    """
    Elimina un miembro del proyecto.
    Solo admin global u owner pueden quitar miembros.
    """
    return service.remove_member(id, id_usuario, user)
