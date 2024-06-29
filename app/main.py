import asyncio
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from admin.router import admin_router
from app.logger_file import logger
from auth.auth_jwt import auth_router
from car_user.router import car_router
from db.orm import SyncOrm
from search.router import search_router

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

app = FastAPI()

app.include_router(admin_router)
app.include_router(car_router)
app.include_router(search_router)
app.include_router(auth_router)


async def initialize_database():
    logger.info("API started")
    sync_orm = SyncOrm()
    sync_orm.drop_tables()
    sync_orm.create_tables()
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="localhost")
