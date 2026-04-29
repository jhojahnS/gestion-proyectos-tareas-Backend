from passlib.context import CryptContext
from jose import jwt
from datetime import UTC, datetime, timedelta

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128

# bcrypt_sha256 supera el límite real de 72 bytes de bcrypt puro.
# Se mantiene "bcrypt" como esquema deprecated para compatibilidad con
# hashes ya almacenados.
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
)


def validate_password_length(password: str) -> None:
    length = len(password)
    if length < PASSWORD_MIN_LENGTH:
        raise ValueError(
            f"La contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres"
        )
    if length > PASSWORD_MAX_LENGTH:
        raise ValueError(
            f"La contraseña no puede superar {PASSWORD_MAX_LENGTH} caracteres"
        )


def hash_password(password: str) -> str:
    validate_password_length(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError:
        return False


def create_access_token(sub: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": sub,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
