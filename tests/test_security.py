from passlib.handlers.bcrypt import bcrypt

from app.core.security import (
    PASSWORD_MAX_LENGTH,
    hash_password,
    validate_password_length,
    verify_password,
)


def test_hash_and_verify_password():
    password = "ClaveSegura123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password) is True


def test_hash_and_verify_long_password_within_new_limit():
    long_password = "a" * PASSWORD_MAX_LENGTH
    hashed_password = hash_password(long_password)

    assert verify_password(long_password, hashed_password) is True


def test_validate_password_length_raises_clear_error_when_limit_exceeded():
    long_password = "a" * (PASSWORD_MAX_LENGTH + 1)

    try:
        validate_password_length(long_password)
    except ValueError as exc:
        assert (
            str(exc)
            == f"La contraseña no puede superar {PASSWORD_MAX_LENGTH} caracteres"
        )
    else:
        raise AssertionError("Se esperaba ValueError para contraseñas demasiado largas")


def test_verify_password_supports_legacy_bcrypt_hashes():
    password = "ClaveSegura123"
    legacy_hash = bcrypt.hash(password)

    assert verify_password(password, legacy_hash) is True

