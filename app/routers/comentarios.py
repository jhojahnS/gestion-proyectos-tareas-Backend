from fastapi import APIRouter, Depends

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
    service: ComentarioService = Depends(),
):
    return service.create(comentario)


@router.get("/", response_model=list[ComentarioResponse])
async def read_comentarios(service: ComentarioService = Depends()):
    return service.get_all()


@router.get("/{id}", response_model=ComentarioResponse)
async def read_comentario(
    id: int,
    service: ComentarioService = Depends(),
):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=ComentarioResponse)
async def update_comentario(
    id: int,
    comentario_data: ComentarioUpdate,
    service: ComentarioService = Depends(),
):
    return service.update(id, comentario_data)


@router.delete("/{id}", response_model=dict)
async def delete_comentario(
    id: int,
    service: ComentarioService = Depends(),
):
    return service.delete(id)
