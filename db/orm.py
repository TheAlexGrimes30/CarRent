import sys
from pathlib import Path
from typing import Optional

from sqlalchemy import select, delete

from app.logger_file import logger
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
        try:
            Base.metadata.drop_all(sync_engine)
            print("Tables deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def create_tables() -> None:
        """
        Метод создаёт таблицы в базе данных
        :return:
        """
        try:
            Base.metadata.create_all(sync_engine)
            print("Tables created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def add_car(car_brand: str, car_model: str, rent_deposit: int, car_class: str,
                drive_unit: str, car_fuel: str, car_year: int, engine_power: int,
                transmission: str, description: str,
                car_number: str, car_photo: str, car_status: str) -> None:
        """
        Метод для добавления нового автомобиля
        :param car_brand:
        :param car_model:
        :param rent_deposit:
        :param car_class:
        :param drive_unit:
        :param car_fuel:
        :param car_year:
        :param engine_power:
        :param transmission:
        :param description:
        :param car_number:
        :param car_photo:
        :param car_status:
        :return:
        """
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
    def get_all_cars(limit: Optional[int] = None, offset: Optional[int] = None):
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
        try:
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
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

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
                       CarsOrm.engine_power, CarsOrm.car_photo).where(CarsOrm.car_class == car_class)

        return SyncOrm.execute_query_for_car(query, limit, offset)

    @staticmethod
    def get_car_by_id_for_admin(car_id: int):
        """
        Метод для получения данных автомобиля (для администратора)
        :param car_id:
        :return:
        """
        try:
            with session_factory() as session:
                query = select(CarsOrm).where(CarsOrm.car_id == car_id)
                result = session.execute(query).first()

                if result is not None:
                    car_instance = result[0]
                    car_data = {column.key: getattr(car_instance, column.key) for column in
                                car_instance.__table__.columns}
                    return car_data
                else:
                    return None
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def get_car_by_id_for_user(car_id: int):
        """
        Метод для получения данных автомобиля (для пользователя)
        :param car_id:
        :return:
        """
        try:
            with session_factory() as session:
                query = select(
                    CarsOrm.car_id,
                    CarsOrm.car_brand,
                    CarsOrm.car_model,
                    CarsOrm.rent_deposit,
                    CarsOrm.car_class,
                    CarsOrm.drive_unit,
                    CarsOrm.car_fuel,
                    CarsOrm.car_year,
                    CarsOrm.engine_power,
                    CarsOrm.transmission,
                    CarsOrm.description,
                    CarsOrm.car_photo
                ).where(CarsOrm.car_id == car_id)

                result = session.execute(query).first()

                if result is not None:
                    car_data = {
                        "car_id": result.car_id,
                        "car_brand": result.car_brand,
                        "car_model": result.car_model,
                        "rent_deposit": result.rent_deposit,
                        "car_class": result.car_class,
                        "drive_unit": result.drive_unit,
                        "car_fuel": result.car_fuel,
                        "car_year": result.car_year,
                        "engine_power": result.engine_power,
                        "transmission": result.transmission,
                        "description": result.description,
                        "car_photo": result.car_photo
                    }
                    return car_data
                else:
                    return None
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def delete_car_by_id(car_id: int) -> None:
        """
        Метод для удаления автомобиля по его id
        :param car_id:
        :return:
        """
        try:
            with session_factory() as session:
                query = delete(CarsOrm).where(CarsOrm.car_id == car_id)
                result = session.execute(query)
                session.commit()
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def update_car_by_id(car_id: int, car_brand: Optional[str] = None, car_model: Optional[str] = None,
                         rent_deposit: Optional[int] = None, car_class: Optional[str] = None,
                         drive_unit: Optional[str] = None, car_fuel: Optional[str] = None,
                         car_year: Optional[int] = None, engine_power: Optional[int] = None,
                         transmission: Optional[str] = None, description: Optional[str] = None,
                         car_number: Optional[str] = None, car_photo: Optional[str] = None,
                         car_status: Optional[str] = None) -> None:
        """
        Метод для редактирования данных автомобиля
        :param car_id:
        :param car_brand:
        :param car_model:
        :param rent_deposit:
        :param car_class:
        :param drive_unit:
        :param car_fuel:
        :param car_year:
        :param engine_power:
        :param transmission:
        :param description:
        :param car_number:
        :param car_photo:
        :param car_status:
        :return:
        """
        try:
            with session_factory() as session:
                car = session.query(CarsOrm).where(CarsOrm.car_id == car_id).one_or_none()

                if car is not None:
                    if car_brand is not None:
                        car.car_brand = car_brand
                    if car_model is not None:
                        car.car_model = car_model
                    if rent_deposit is not None:
                        car.rent_deposit = rent_deposit
                    if car_class is not None:
                        car.car_class = car_class
                    if drive_unit is not None:
                        car.drive_unit = drive_unit
                    if car_fuel is not None:
                        car.car_fuel = car_fuel
                    if car_year is not None:
                        car.car_year = car_year
                    if engine_power is not None:
                        car.engine_power = engine_power
                    if transmission is not None:
                        car.transmission = transmission
                    if description is not None:
                        car.description = description
                    if car_number is not None:
                        car.car_number = car_number
                    if car_photo is not None:
                        car.car_photo = car_photo
                    if car_status is not None:
                        car.car_status = car_status

                    session.commit()
                else:
                    print(f"Car with id {car_id} not found.")
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

