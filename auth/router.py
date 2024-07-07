import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from starlette.status import HTTP_401_UNAUTHORIZED

from app.logger_file import logger
from auth.schemas import UserResponse, Token
from auth.utils import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from db.orm import SyncOrm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

sync_orm = SyncOrm()


@auth_router.post("/signup", response_model=UserResponse)
def signup(username: str, email: str, password: str, is_admin: bool):
    signup_exception = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error with sign up")
    try:
        if "@" not in email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")

        if len(password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password too short, must be at least 8 characters")
        hashed_password = get_password_hash(password).encode('utf-8')
        sync_orm.add_user(username, email, hashed_password, is_admin)
        user = sync_orm.get_user(email)
        return UserResponse(
            id=user.user_id,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
    except Exception:
        raise signup_exception


@auth_router.post("/signin", response_model=Token)
def signin(email: str = Form(...), password: str = Form(...)):
    try:
        logger.info(f"Attempting signin for email: {email}")

        user = sync_orm.get_user(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        logger.info(f"User found with email: {email}")
        jwt_payload = {
            'sub': user.username,
            'email': user.email
        }
        access_token = create_access_token(data=jwt_payload)
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error during signin: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials. Error: {e}")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = sync_orm.get_user(email)
        if user is None:
            raise credentials_exception
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except Exception as e:
        logger.error(f"Error during token validation: {e}")
        raise credentials_exception


@auth_router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
