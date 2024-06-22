import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter

from app.logger_file import logger
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

search_router = APIRouter(
    prefix="/search",
    tags=['search']
)


@search_router.get("/search")
def search_car(search_string: Optional[str] = None, limit: Optional[int] = None,
               offset: Optional[int] = None):
    """
    Метод для работы с поиском
    :param search_string: 
    :param limit:
    :param offset:
    :return:
    """
    result = SyncOrm.get_search_data(search_string, limit, offset)
    logger.info("Car data was searched")
    return{
        'data': result,
        'status': 'ok'
    }
