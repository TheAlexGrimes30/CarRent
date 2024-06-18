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

        try:
            with session_factory() as session:
                session.add_all([car])
                session.commit()
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def get_cars_by_brand(car_brand: str, limit: Optional[int] = None, offset: Optional[int] = None) -> dict:
        """
        Метод для вывода автомобилей по бренду
        :param car_brand:
        :param limit:
        :param offset:
        :return:
        """
        query = select(CarsOrm.car_id, CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                       CarsOrm.drive_unit, CarsOrm.car_year,
                       CarsOrm.engine_power, CarsOrm.car_photo).where(CarsOrm.car_brand == car_brand)

        return SyncOrm.execute_query_for_car(query, limit, offset)

    @staticmethod
    def get_all_car(limit: Optional[int] = None, offset: Optional[int] = None):
        """
        Метод для вывода всех автомобилей
        :param limit:
        :param offset:
        :return:
        """
        query = select(CarsOrm.car_id, CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                       CarsOrm.drive_unit, CarsOrm.car_year,
                       CarsOrm.engine_power, CarsOrm.car_photo)

        return SyncOrm.execute_query_for_car(query, limit, offset)

    @staticmethod
    def execute_query_for_car(query, limit: Optional[int] = None, offset: Optional[int] = None) -> dict:
        """
        Метод для выполнения запросов для CarsORM
        :param query:
        :param limit:
        :param offset:
        :return:
        """
        with session_factory() as session:
            if limit is not None:
                query = query.limit(limit=limit)

            if offset is not None:
                query = query.offset(offset=offset)

            result = session.execute(query).all()
            result_dict = dict()

            for element in result:
                result_dict[element.car_id] = {
                    "car_brand": element.car_brand,
                    "car_model": element.car_model,
                    "rent_deposit": element.rent_deposit,
                    "drive_unit": element.drive_unit,
                    "car_year": element.car_year,
                    "engine_power": element.engine_power,
                    "car_photo": element.car_photo
                }
            return result_dict

    @staticmethod
    def get_cars_by_class(car_class: str, limit: Optional[int] = None, offset: Optional[int] = None) -> dict:
        """
        Вывод автомобилей по их классам
        :param car_class:
        :param limit:
        :param offset:
        :return:
        """
        query = select(CarsOrm.car_id, CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                       CarsOrm.drive_unit, CarsOrm.car_year,
                       CarsOrm.engine_power).where(CarsOrm.car_class == car_class)

        return SyncOrm.execute_query_for_car(query, limit, offset)

    @staticmethod
    def get_car_by_id_in_admin(car_id: int):
        with session_factory() as session:
            query = select(CarsOrm).where(CarsOrm.car_id == car_id)
            result = session.execute(query).first()

            if result is not None:
                car_data = dict(result)
                return car_data
            else:
                return None

