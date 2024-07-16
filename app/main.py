import asyncio
import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

from admin.router import admin_router
from app.logger_file import logger
from auth.manager import get_user_manager, UserManager
from auth.schemas import UserRead, UserCreate
from auth.utils import auth_backend
from car_user.router import car_router
from chat.router import chat_router
from db.models import UserOrm
from fastapi.staticfiles import StaticFiles
from search.router import search_router

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

app = FastAPI()

fastapi_users = FastAPIUsers[UserOrm, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: UserOrm = Depends(current_user)):
    return {"username": user.username, "email": user.email, "is_superuser": user.is_superuser}


@app.delete("/users/delete/me", response_model=dict)
async def delete_me(
        user: UserOrm = Depends(current_user),
        user_manager: UserManager = Depends(get_user_manager),
):
    await user_manager.delete(user)
    return {"status": "User deleted successfully"}


app.include_router(admin_router)
app.include_router(car_router)
app.include_router(search_router)
app.include_router(chat_router)


async def initialize_database():
    logger.info("API started")
    logger.info("Database initialization complete")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(initialize_database())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API stopped")


@app.get("/")
async def root():
    return {"message": "Hello World"}


static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"Created static directory at {static_dir}")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="localhost")
