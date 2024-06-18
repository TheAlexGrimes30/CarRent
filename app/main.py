import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logger_file import logger
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

app = FastAPI()


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


@app.on_event('stastup')
async def server_start():
    logger.info("API started")
    sync_orm = SyncOrm()
    sync_orm.drop_tables()
    sync_orm.crate_tables()

if __name__ == "__main__":
    uvicorn.run(app, port=5432, host="localhost")