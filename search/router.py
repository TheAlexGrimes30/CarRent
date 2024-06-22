import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter

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
    result = SyncOrm.get_search_data(search_string, limit, offset)
    return{
        'data': result,
        'status': 'ok'
    }
