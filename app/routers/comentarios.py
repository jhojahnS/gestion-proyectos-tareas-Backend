from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

from app.schemas.comentario import (
    ComentarioCreate,
    ComentarioResponse,
    ComentarioUpdate,
)
from app.services.comentario_service import ComentarioService

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])


@router.post("/", response_model=ComentarioResponse)
async def create_comentario(
    comentario: ComentarioCreate,
    user=Depends(get_current_user),
    service: ComentarioService = Depends(),
):
    """
    Crea un comentario.
    Solo miembros del proyecto pueden comentar.
    """
    return service.create(comentario, user)


@router.get("/", response_model=list[ComentarioResponse])
async def read_comentarios(
    user=Depends(get_current_user),
    service: ComentarioService = Depends()
):
    """
    Lista comentarios:
    - Admin global: todos los comentarios
    - Usuario normal: comentarios de proyectos donde es miembro
    """
    return service.get_all(user)


@router.get("/{id}", response_model=ComentarioResponse)
async def read_comentario(
    id: int,
    user=Depends(get_current_user),
    service: ComentarioService = Depends(),
):
    """
    Obtiene un comentario por ID.
    Solo admin o miembros del proyecto pueden verlo.
    """
    return service.get_by_id(id, user)


@router.patch("/{id}", response_model=ComentarioResponse)
async def update_comentario(
    id: int,
    comentario_data: ComentarioUpdate,
    user=Depends(get_current_user),
    service: ComentarioService = Depends(),
):
    """
    Actualiza un comentario.
    Solo el autor del comentario o admin pueden editar.
    """
    return service.update(id, comentario_data, user)


@router.delete("/{id}", response_model=dict)
async def delete_comentario(
    id: int,
    user=Depends(get_current_user),
    service: ComentarioService = Depends(),
):
    """
    Elimina un comentario.
    Solo el autor del comentario o admin pueden borrar.
    """
    return service.delete(id, user)
