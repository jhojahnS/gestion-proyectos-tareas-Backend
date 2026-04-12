from fastapi import APIRouter, Depends
from app.services.proyecto_service import ProyectoService
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse, ProyectoUpdate

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProyectoResponse)
async def create_proyecto(proyecto: ProyectoCreate, service: ProyectoService = Depends()):
    return service.create(proyecto)


@router.get("/", response_model=list[ProyectoResponse])
async def read_proyectos(service: ProyectoService = Depends()):
    return service.get_all()


@router.get("/{id}", response_model=ProyectoResponse)
async def read_proyecto(id: int, service: ProyectoService = Depends()):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=ProyectoResponse)
async def update_proyecto(id: int, proyecto_data: ProyectoUpdate, service: ProyectoService = Depends()):
    return service.update(id, proyecto_data)


@router.delete("/{id}", response_model=dict)
async def delete_proyecto(id: int, service: ProyectoService = Depends()):
    return service.delete(id)
