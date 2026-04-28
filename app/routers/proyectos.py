from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoResponse,
    ProyectoUpdate,
)
from app.services.proyecto_service import ProyectoService

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProyectoResponse)
async def create_proyecto(
    proyecto: ProyectoCreate,
    user=Depends(get_current_user),
    service: ProyectoService = Depends(),
):
    return service.create(proyecto, user.id_usuario)


@router.get("/")
def read_proyectos(
    user=Depends(get_current_user),
    service: ProyectoService = Depends()
):
    return service.get_by_user(user.id_usuario)


@router.get("/{id}", response_model=ProyectoResponse)
async def read_proyecto(
    id: int,
    service: ProyectoService = Depends(),
):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=ProyectoResponse)
async def update_proyecto(
    id: int,
    proyecto_data: ProyectoUpdate,
    service: ProyectoService = Depends(),
):
    return service.update(id, proyecto_data)


@router.delete("/{id}", response_model=dict)
async def delete_proyecto(
    id: int,
    service: ProyectoService = Depends(),
):
    return service.delete(id)
