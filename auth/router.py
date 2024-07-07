import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from app.logger_file import logger
from auth.schemas import UserResponse, Token
from auth.utils import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from db.orm import SyncOrm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

sync_orm = SyncOrm()


@auth_router.post("/signup", response_model=UserResponse)
def signup(username: str, email: str, password: str, is_active: bool, is_admin: bool):
    try:
        hashed_password = get_password_hash(password).encode('utf-8')
        sync_orm.add_user(username, email, hashed_password, is_active, is_admin)
        user = sync_orm.get_user(email)
        return UserResponse(
            id=user.user_id,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")


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


@auth_router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info(f"Received token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded payload: {payload}")
        username: str = payload.get("sub")
        email: str = payload.get("email")

        if username is None or email is None:
            logger.warning("Invalid token: Missing username or email")
            raise credential_exception

        user = sync_orm.get_user(email)
        if user is None:
            logger.warning("User not found")
            raise credential_exception

        return UserResponse(
            id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )

    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired",
                            headers={"WWW-Authenticate": "Bearer"})

    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        raise credential_exception

    except Exception as e:
        logger.error(f"Exception while reading current user data: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Server error: {str(e)}")


