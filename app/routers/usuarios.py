from fastapi import APIRouter, Depends, Query

from app.core.auth import get_current_user
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse)
async def create_usuario(
    usuario: UsuarioCreate,
    service: UsuarioService = Depends(),
):
    return service.create(usuario)


@router.get("/", response_model=list[UsuarioResponse])
async def read_usuarios(service: UsuarioService = Depends()):
    return service.get_all()


@router.get("/buscar", response_model=list[UsuarioResponse])
async def search_usuarios(
    email: str = Query(..., min_length=1),
    user=Depends(get_current_user),
    service: UsuarioService = Depends(),
):
    """
    Busca usuarios cuyo email contenga el texto recibido.
    Requiere autenticación. Máximo 10 resultados.
    """
    return service.search_by_email(email)


@router.get("/{id}", response_model=UsuarioResponse)
async def read_usuario(
    id: int,
    service: UsuarioService = Depends(),
):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=UsuarioResponse)
async def update_usuario(
    id: int,
    usuario_data: UsuarioUpdate,
    service: UsuarioService = Depends(),
):
    return service.update(id, usuario_data)


@router.delete("/{id}", response_model=dict)
async def delete_usuario(
    id: int,
    service: UsuarioService = Depends(),
):
    return service.delete(id)
