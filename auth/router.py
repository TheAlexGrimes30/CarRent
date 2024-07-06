from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from auth.schemas import UserResponse, Token
from auth.utils import get_password_hash, verify_password, create_access_token
from db.orm import SyncOrm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

sync_orm = SyncOrm()


@auth_router.post("/signup", response_model=UserResponse)
def signup(username: str, email: str, password: str, is_active: str, is_admin: str):
    try:
        hashed_password = get_password_hash(password)
        sync_orm.add_user(username, email, hashed_password, is_active, is_admin)
        return {
            'message': "User was signed up",
            'status': 'ok'
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")


@auth_router.post("/signin", response_model=Token)
def signin(email: str = Form(), password: str = Form()):
    try:
        user = sync_orm.get_user(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User was not found")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")

        jwt_payload = {
            'sub': user.username,
            'email': user.email
        }

        access_token = create_access_token(data=jwt_payload)
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Wrong password. Error: {e}")
