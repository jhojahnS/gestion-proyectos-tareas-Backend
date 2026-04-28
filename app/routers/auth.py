from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import UsuarioService
from app.core.security import verify_password, create_access_token
from app.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UsuarioResponse)
def register(user: UsuarioCreate, service: UsuarioService = Depends()):
    return service.create(user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioService = Depends(),
):
    user = service.get_by_email(form_data.username)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UsuarioResponse)
def me(user=Depends(get_current_user)):
    return user
