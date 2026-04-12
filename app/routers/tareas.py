from fastapi import APIRouter, Depends
from app.services.tarea_service import TareaService
from app.schemas.tarea import TareaCreate, TareaResponse, TareaUpdate

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/", response_model=TareaResponse)
async def create_tarea(tarea: TareaCreate, service: TareaService = Depends()):
    return service.create(tarea)


@router.get("/", response_model=list[TareaResponse])
async def read_tareas(service: TareaService = Depends()):
    return service.get_all()


@router.get("/{id}", response_model=TareaResponse)
async def read_tarea(id: int, service: TareaService = Depends()):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=TareaResponse)
async def update_tarea(id: int, tarea_data: TareaUpdate, service: TareaService = Depends()):
    return service.update(id, tarea_data)


@router.delete("/{id}", response_model=dict)
async def delete_tarea(id: int, service: TareaService = Depends()):
    return service.delete(id)
