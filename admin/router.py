import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter

from app.logger_file import logger
from db.orm import SyncOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

sync_orm = SyncOrm()
BASE_DIR = Path(__file__).parent


@admin_router.get('/all_car')
def get_all_cars(limit: Optional[int] = None, offset: Optional[int] = None):
    result = sync_orm.get_all_cars(limit, offset)
    logger.info(f"All cars with limit={limit} and offset={offset}")
    return {
        'data': result,
        'status': 'ok'
    }


@admin_router.post('/add_car')
def add_car(car_brand: str, car_model: str, rent_deposit: int, car_class: str,
            drive_unit: str, car_fuel: str, car_year: int, engine_power: int,
            transmission: str, description: str,
            car_number: str, car_photo: str, car_status: str):
    sync_orm.add_car(car_brand, car_model, rent_deposit, car_class,
                     drive_unit, car_fuel, car_year, engine_power,
                     transmission, description,
                     car_number, car_photo, car_status)

    logger.info("New car was added")
    return {
        'status': 'ok'
    }


@admin_router.put('/update_car/{car_id}')
def update_car(car_id: int, car_brand: Optional[str] = None, car_model: Optional[str] = None,
               rent_deposit: Optional[int] = None, car_class: Optional[str] = None,
               drive_unit: Optional[str] = None, car_fuel: Optional[str] = None,
               car_year: Optional[int] = None, engine_power: Optional[int] = None,
               transmission: Optional[str] = None, description: Optional[str] = None,
               car_number: Optional[str] = None, car_photo: Optional[str] = None,
               car_status: Optional[str] = None):
    sync_orm.update_car_by_id(car_id, car_brand, car_model, rent_deposit, car_class, drive_unit, car_fuel,
                              car_year, engine_power, transmission, description,
                              car_number, car_photo, car_status)

    logger.info(f"Car with {car_id} was updated")
    return {
        'status': 'ok'
    }


@admin_router.delete('/delete_car/{car_id}')
def delete_car(car_id: int):
    sync_orm.delete_car_by_id(car_id)
    logger.info(f"Car with {car_id} was deleted")
    return {
        'status': 'ok'
    }


@admin_router.get('/get_car/{car_id}')
def get_car_by_id(car_id: int):
    result = sync_orm.get_car_by_id_for_admin(car_id)
    logger.info(f"Car with {car_id}")
    return{
        'data': result,
        'status': 'ok'
    }
