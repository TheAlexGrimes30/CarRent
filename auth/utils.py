from datetime import timedelta, datetime

import bcrypt
import jwt

from auth.config import settings
from typing import Union


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_timedelta: Union[timedelta, None] = None,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes):
    """
    Генерация токена
    :param payload:
    :param private_key:
    :param algorithm:
    :param expire_timedelta:
    :param expire_minutes:
    :return:
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(token: Union[str, bytes],
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm):
    """
    Чтение и валидация токена
    :param token:
    :param public_key:
    :param algorithm:
    :return:
    """

    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Метод для хэширования пароля
    :param password:
    :return:
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes):
    """
    Метод для валидации пароля
    :param password:
    :param hashed_password:
    :return:
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
