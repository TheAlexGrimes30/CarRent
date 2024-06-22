import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter

from app.logger_file import logger
from car_user.filters import filter_car_data
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

BASE_DIR = Path(__file__).parent

sync_orm = SyncOrm()


@car_router.get("/all_cars")
def get_all_cars(limit: Optional[int] = None, offset: Optional[int] = None, min_rent: Optional[int] = None,
                 max_rent: Optional[int] = None, car_brand: Optional[str] = None,
                 car_model: Optional[str] = None, drive_unit: Optional[str] = None,
                 min_year: Optional[int] = None, max_year: Optional[int] = None,
                 min_engine_power: Optional[int] = None, max_engine_power: Optional[int] = None,
                 transmission: Optional[str] = None, car_fuel: Optional[str] = None,
                 car_class: Optional[str] = None, car_status: Optional[str] = None):
    """
    Метод для вывода авто пользователю с применением фильтрации
    :param limit:
    :param offset:
    :param min_rent:
    :param max_rent:
    :param car_brand:
    :param car_model:
    :param drive_unit:
    :param min_year:
    :param max_year:
    :param min_engine_power:
    :param max_engine_power:
    :param transmission:
    :param car_fuel:
    :param car_class:
    :param car_status:
    :return:
    """
    if limit is not None:
        if limit < 0:
            return {
                'status': 'error',
                'description': 'limit must not be less than 0'
            }

    if offset is not None:
        if offset < 0:
            return {
                'status': 'error',
                'description': 'offset must not be less than 0'
            }

    validation_errors = filter_car_data(min_rent,
                                        max_rent, drive_unit,
                                        min_year, max_year,
                                        min_engine_power, max_engine_power,
                                        transmission, car_fuel,
                                        car_class, car_brand, car_model,
                                        car_status)

    if validation_errors:
        return {
            'status': 'error',
            'description': validation_errors
        }

    result = sync_orm.get_all_cars_for_user(limit, offset, min_rent,
                                            max_rent, car_brand,
                                            car_model, drive_unit,
                                            min_year, max_year,
                                            min_engine_power, max_engine_power,
                                            transmission, car_fuel,
                                            car_class, car_status)

    logger.info(f"All cars with limit={limit} and offset={offset}")
    return {
        'data': result,
        'status': 'ok'
    }


@car_router.get("/all_cars/{car_id}")
def get_car_by_id(car_id: int):
    """
    Метод для вывода данных авто по id
    :param car_id:
    :return:
    """
    result = sync_orm.get_car_by_id_for_user(car_id)
    logger.info(f"Car with id={car_id}")
    return {
        'data': result,
        'status': 'ok'
    }
