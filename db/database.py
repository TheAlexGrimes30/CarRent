import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.config import settings
from db.models import UserOrm

DIR_PATH = Path(__file__).parent.parent
sys.path.append(str(DIR_PATH))

engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserOrm)
