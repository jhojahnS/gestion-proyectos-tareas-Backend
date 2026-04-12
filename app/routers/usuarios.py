from fastapi import APIRouter, Depends
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse)
async def create_usuario(usuario: UsuarioCreate, service: UsuarioService = Depends()):
    return service.create(usuario)


@router.get("/", response_model=list[UsuarioResponse])
async def read_usuarios(service: UsuarioService = Depends()):
    return service.get_all()


@router.get("/{id}", response_model=UsuarioResponse)
async def read_usuario(id: int, service: UsuarioService = Depends()):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=UsuarioResponse)
async def update_usuario(id: int, usuario_data: UsuarioUpdate, service: UsuarioService = Depends()):
    return service.update(id, usuario_data)


@router.delete("/{id}", response_model=dict)
async def delete_usuario(id: int, service: UsuarioService = Depends()):
    return service.delete(id)