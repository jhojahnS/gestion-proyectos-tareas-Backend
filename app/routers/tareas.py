from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

from app.schemas.tarea import TareaCreate, TareaResponse, TareaUpdate
from app.services.tarea_service import TareaService

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/", response_model=TareaResponse)
async def create_tarea(
    tarea: TareaCreate,
    user=Depends(get_current_user),
    service: TareaService = Depends(),
):
    """
    Crea una tarea.
    Solo owner, editor o admin pueden crear tareas.
    """
    return service.create(tarea, user)


@router.get("/", response_model=list[TareaResponse])
async def read_tareas(
    user=Depends(get_current_user),
    service: TareaService = Depends()
):
    """
    Lista tareas:
    - Admin global: todas las tareas
    - Usuario normal: tareas de proyectos donde es miembro
    """
    return service.get_all(user)


@router.get("/{id}", response_model=TareaResponse)
async def read_tarea(
    id: int,
    user=Depends(get_current_user),
    service: TareaService = Depends(),
):
    """
    Obtiene una tarea por ID.
    Solo admin o miembros del proyecto pueden verla.
    """
    return service.get_by_id(id, user)


@router.patch("/{id}", response_model=TareaResponse)
async def update_tarea(
    id: int,
    tarea_data: TareaUpdate,
    user=Depends(get_current_user),
    service: TareaService = Depends(),
):
    """
    Actualiza una tarea.
    Solo owner, editor o admin pueden editar.
    """
    return service.update(id, tarea_data, user)


@router.delete("/{id}", response_model=dict)
async def delete_tarea(
    id: int,
    user=Depends(get_current_user),
    service: TareaService = Depends(),
):
    """
    Elimina una tarea.
    Solo owner, editor o admin pueden borrar.
    """
    return service.delete(id, user)
