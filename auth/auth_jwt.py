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
        email: str = Form(...),
        password: str = Form(...),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

    try:
        user = sync_orm.get_user(email)
        if not user:
            raise unauthed_exc

        user_schema = UserSchema(
            username=user[0],
            email=user[1],
            password=user[2],
            driving_licence_date=user[3],
            gibdd_number=user[4],
            driving_licence_number=user[5],
            balance=user[6],
            active=user[7]
        )

        hashed_password = user[2]
        if not validate_password(
                password=password,
                hashed_password=hashed_password
        ):
            raise unauthed_exc

        if not user_schema.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User inactive"
            )

        return user_schema

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        ) from e


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


def get_current_token_payload_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'invalid token error {e}')

    return payload


def get_current_auth_user(payload: dict = Depends(get_current_token_payload_user)) -> UserSchema:
    try:
        user_email: str | None = payload.get('email')
        user = sync_orm.get_user(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='token invalid (user not found)'
            )
        user = UserSchema(
            username=user[0],
            email=user[1],
            password=user[2]
        )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    try:
        if user.active:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive'
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@auth_router.get('/users/me')
def auth_user_check_self_info(user: UserSchema = Depends(get_current_active_auth_user)):
    try:
        return {
            'username': user.username,
            'email': user.email
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@auth_router.post('/registration')
def user_registration(username: str, user_email: str, password: str,
                      driving_licence_date: str, gibdd_number: str,
                      driving_licence_number: str, balance: int):

    if not validate_password_strength(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and contain at least"
                   " one uppercase letter, one digit, and one special character."
        )

    hashed_password = hash_password(password)
    sync_orm.add_user(username, user_email, hashed_password, driving_licence_date, gibdd_number,
                      driving_licence_number, balance)
    return {
        'data': None,
        'status': 'ok'
    }


def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?/~]', password):
        return False

    return True
