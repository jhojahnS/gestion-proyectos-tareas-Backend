from fastapi import APIRouter, Depends
from app.services.rol_service import RolService
from app.schemas.rol import RolCreate, RolResponse, RolUpdate

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RolResponse)
async def create_rol(rol: RolCreate, service: RolService = Depends()):
    return service.create(rol)


@router.get("/", response_model=list[RolResponse])
async def read_roles(service: RolService = Depends()):
    return service.get_all()


@router.get("/{id}", response_model=RolResponse)
async def read_rol(id: int, service: RolService = Depends()):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=RolResponse)
async def update_rol(id: int, rol_data: RolUpdate, service: RolService = Depends()):
    return service.update(id, rol_data)


@router.delete("/{id}", response_model=dict)
async def delete_rol(id: int, service: RolService = Depends()):
    return service.delete(id)
