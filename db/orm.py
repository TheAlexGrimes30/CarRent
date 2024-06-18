import sys
from pathlib import Path
from typing import Optional

from sqlalchemy import select

from db.database import sync_engine, session_factory
from db.models import Base, CarsOrm

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))


class SyncOrm(object):
    """
    Класс для работы с базой данных
    с применением паттерна Singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def drop_tables() -> None:
        """
        Метод удаляет все таблицы в базе данных
        :return:
        """
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def crate_tables() -> None:
        """
        Метод создаёт таблицы в базе данных
        :return:
        """
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def add_car(car_brand: str, car_model: str, rent_deposit: int, car_class: str,
                drive_unit: str, car_fuel: str, car_year: int, engine_power: int,
                transmission: str, description: str,
                car_number: str, car_photo: str, car_status: str) -> None:
        car = CarsOrm(
            car_brand=car_brand,
            car_model=car_model,
            rent_deposit=rent_deposit,
            car_class=car_class,
            drive_unit=drive_unit,
            car_fuel=car_fuel,
            car_year=car_year,
            engine_power=engine_power,
            transmission=transmission,
            description=description,
            car_number=car_number,
            car_photo=car_photo,
            car_status=car_status
        )

        with session_factory() as session:
            session.add_all([car])
            session.commit()

    @staticmethod
    def get_car_by_brand(car_brand: str, limit: Optional[int] = None, offset: Optional[int] = None) -> dict:
        with session_factory() as session:
            query = select(CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                           CarsOrm.drive_unit, CarsOrm.car_year,
                           CarsOrm.engine_power).where(CarsOrm.car_brand == car_brand)
            if limit is not None:
                query = query.limit(limit=limit)

            if offset is not None:
                query = query.offset(offset=offset)

            result = session.execute(query).scalars().all()
            result_dict = dict()

            for index, element in enumerate(result):
                result_dict[index] = {
                    "car_brand": element.car_brand,
                    "car_model": element.car_model,
                    "rent_deposit": element.rent_deposit,
                    "drive_unit": element.drive_unit,
                    "car_year": element.car_year,
                    "engine_power": element.engine_power
                }
            return result_dict
