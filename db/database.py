import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.config import settings

DIR_PATH = Path(__file__).parent.parent
sys.path.append(str(DIR_PATH))

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False
)

session_factory = sessionmaker(sync_engine)
