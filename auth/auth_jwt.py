from __future__ import annotations

import re
import sys
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from pydantic import BaseModel

from app.logger_file import logger
from auth.schemas import UserSchema
from auth.utils import validate_password, encode_jwt, decode_jwt, hash_password
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

http_bearer = HTTPBearer()

oauth2_bearer = OAuth2PasswordBearer('/token')

sync_orm = SyncOrm()


class Token(BaseModel):
    access_token: str
    token_type: str


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def validate_auth_user(
        email: str = Form(),
        password: str = Form(),
):
    try:
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

        user = sync_orm.get_user(email)
        if not user:
            raise unauthed_exc

        hashed_password = user.hashed_password
        print(hashed_password)

        user_schema = UserSchema(username=user.username, email=user.email,
                                 password=user.hashed_password, driving_licence_date=user.driving_licence_date,
                                 gibdd_number=user.gibdd_number, driving_licence_number=user.driving_licence_number,
                                 balance=user.balance)

        if not validate_password(password, hashed_password):
            raise unauthed_exc

        if not user_schema.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user inactive",
            )

        return user_schema
    except Exception as e:
        print(f"Error: {e}")
        raise


@auth_router.post('/login/', response_model=Token)
async def auth_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        'sub': user.username,
        'email': user.email
    }
    token = encode_jwt(jwt_payload)
    logger.info(f'The user {user.username}/{user.email} has logged in')
    return Token(
        access_token=token,
        token_type='Bearer'
    )


@auth_router.post('/registration')
def user_registration(username: str, user_email: str, password: str,
                      driving_licence_date: str, gibdd_number: str,
                      driving_licence_number: str, balance: int):
    hashed_password = hash_password(password)
    sync_orm.add_user(username, user_email, hashed_password, driving_licence_date, gibdd_number,
                      driving_licence_number, balance)
    return {
        'data': None,
        'status': 'ok'
    }
