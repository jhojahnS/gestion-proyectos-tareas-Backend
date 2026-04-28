from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.security import SECRET_KEY, ALGORITHM
from app.services.usuario_service import UsuarioService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UsuarioService = Depends()
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        user = service.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no existe")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")