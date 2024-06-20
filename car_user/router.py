import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter

from app.logger_file import logger
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

BASE_DIR = Path(__file__).parent

sync_orm = SyncOrm()


@car_router.get("/all_car")
def get_all_cars(limit: Optional[int] = None, offset: Optional[int] = None):
    result = sync_orm.get_all_cars(limit, offset)
    logger.info(f"All cars with limit={limit} and offset={offset}")
    return {
        'data': result,
        'status': 'ok'
    }


@car_router.get("/all_cars/{car_brand}")
def get_cars_by_brand(car_brand: str, limit: Optional[int] = None, offset: Optional[int] = None):
    result = sync_orm.get_cars_by_brand(car_brand, limit, offset)
    logger.info(f"Cars {car_brand} with limit={limit} and offset={offset}")
    return {
        'data': result,
        'status': 'ok'
    }


@car_router.get("/all_cars/{car_class}")
def get_cars_by_class(car_class: str, limit: Optional[int] = None, offset: Optional[int] = None):
    result = sync_orm.get_cars_by_class(car_class, limit, offset)
    logger.info(f"Cars {car_class} with limit={limit} and offset={offset}")
    return {
        'data': result,
        'status': 'ok'
    }


@car_router.get("/all_car/{car_id}")
def get_car_by_id(car_id: int):
    car_data_by_id(car_id)


@car_router.get("/all_cars/{car_class}/{car_id}")
def get_class_car_by_id(car_id: int):
    car_data_by_id(car_id)


@car_router.get("all_car/{car_brand}/{car_id}")
def get_brand_car_by_id(car_id: int):
    car_data_by_id(car_id)


def car_data_by_id(car_id: int):
    result = sync_orm.get_car_by_id_for_user(car_id)
    logger.info(f"Car with id={car_id}")
    return {
        'data': result,
        'status': 'ok'
    }
