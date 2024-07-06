import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import select, delete, or_
from sqlalchemy.exc import SQLAlchemyError

from db.database import sync_engine, session_factory
from db.models import Base, CarsOrm, UserOrm

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
    def get_all_cars_for_admin(limit: Optional[int] = None, offset: Optional[int] = None):
        """
        Метод для вывода всех автомобилей админу
        :param limit:
        :param offset:
        :return:
        """
        query = select(CarsOrm.car_id, CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                       CarsOrm.drive_unit, CarsOrm.car_year, CarsOrm.transmission,
                       CarsOrm.engine_power, CarsOrm.car_photo)
        return SyncOrm.execute_query_for_car(query, limit, offset)

    @staticmethod
    def get_all_cars_for_user(limit: Optional[int] = None, offset: Optional[int] = None, min_rent: Optional[int] = None,
                              max_rent: Optional[int] = None, car_brand: Optional[str] = None,
                              car_model: Optional[str] = None, drive_unit: Optional[str] = None,
                              min_year: Optional[int] = None, max_year: Optional[int] = None,
                              min_engine_power: Optional[int] = None, max_engine_power: Optional[int] = None,
                              transmission: Optional[str] = None, car_fuel: Optional[str] = None,
                              car_class: Optional[str] = None, car_status: Optional[str] = None):
        """
        Метод для вывода всех автомобилей пользователю с применением фильтрации
        :param car_status:
        :param car_class:
        :param car_fuel:
        :param transmission:
        :param max_engine_power:
        :param min_engine_power:
        :param max_year:
        :param min_year:
        :param drive_unit:
        :param car_model:
        :param car_brand:
        :param max_rent:
        :param min_rent:
        :param limit:
        :param offset:
        :return:
        """
        query = select(CarsOrm.car_id, CarsOrm.car_brand, CarsOrm.car_model, CarsOrm.rent_deposit,
                       CarsOrm.drive_unit, CarsOrm.car_year, CarsOrm.transmission,
                       CarsOrm.engine_power, CarsOrm.car_photo)

        if min_rent:
            query = query.where(CarsOrm.rent_deposit >= min_rent)

        if max_rent:
            query = query.where(CarsOrm.rent_deposit <= max_rent)

        if min_rent and max_rent:
            if min_rent == max_rent:
                query = query.where(CarsOrm.rent_deposit == min_rent)

        if car_brand:
            query = query.where(CarsOrm.car_brand == car_brand)

        if car_model:
            query = query.where(CarsOrm.car_model == car_model)

        if drive_unit:
            query = query.where(CarsOrm.drive_unit == drive_unit)

        if min_year:
            query = query.where(CarsOrm.car_year >= min_year)

        if max_year:
            query = query.where(CarsOrm.car_year <= max_year)

        if min_year and max_year:
            if min_year == max_year:
                query = query.where(CarsOrm.car_year == min_year)

        if min_engine_power:
            query = query.where(CarsOrm.engine_power <= min_engine_power)

        if max_engine_power:
            query = query.where(CarsOrm.engine_power >= max_engine_power)

        if min_engine_power and max_engine_power:
            if min_engine_power == max_engine_power:
                query = query.where(CarsOrm.engine_power == min_engine_power)

        if transmission:
            query = query.where(CarsOrm.transmission == transmission)

        if car_fuel:
            query = query.where(CarsOrm.car_fuel == car_fuel)

        if car_class:
            query = query.where(CarsOrm.car_class == car_class)

        if car_status:
            query = query.where(CarsOrm.car_status == car_status)

        if car_brand:
            query = query.where(CarsOrm.car_brand == car_brand)

        if car_model:
            query = query.where(CarsOrm.car_model == car_model)

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
                session.execute(query)
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

    @staticmethod
    def get_all_brands():
        """
        Метод, возвращающий список всех брендов авто
        :return:
        """
        return SyncOrm.get_brands_or_models(CarsOrm.car_brand)

    @staticmethod
    def get_all_models():
        """
        Метод, возвращающий список всех моделей авто
        :return:
        """
        return SyncOrm.get_brands_or_models(CarsOrm.car_model)

    @staticmethod
    def get_brands_or_models(data_for_query):
        """
        Метод, для возврата данных бренда или моделей авто
        :param data_for_query:
        :return:
        """
        try:
            with session_factory() as session:
                query = select(data_for_query).distinct()
                result = session.execute(query).all()
                result_list = [row[0] for row in result]
            return result_list
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def get_search_data(search_string: Optional[str] = None, limit: Optional[int] = None,
                        offset: Optional[int] = None):
        """
        Метод для работы с поиском
        :param search_string:
        :param limit:
        :param offset:
        :return:
        """

        try:
            with session_factory() as session:
                query = select(CarsOrm)
                if search_string:
                    search_terms = search_string.split()
                    if len(search_terms) == 1:
                        search_term = f"%{search_terms[0]}%"
                        query = query.where(or_(CarsOrm.car_brand.ilike(search_term),
                                                CarsOrm.car_model.ilike(search_term)))

                    elif len(search_terms) > 1:
                        brand_term = f"%{search_terms[0]}%"
                        model_term = f"%{search_terms[1]}%"
                        query = query.where(CarsOrm.car_brand.ilike(brand_term)).where(
                            CarsOrm.car_model.ilike(model_term))
                if limit:
                    query = query.limit(limit)
                if offset:
                    query = query.offset(offset)
                result = session.execute(query).scalars().all()

                if not result:
                    return []

            return result
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def get_user(email: str):
        try:
            with session_factory() as session:
                query = select(
                    UserOrm.user_id,
                    UserOrm.username,
                    UserOrm.email,
                    UserOrm.hashed_password,
                    UserOrm.is_active,
                    UserOrm.is_admin
                ).where(UserOrm.email == email)

                result = session.execute(query).first()
                return result
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

    @staticmethod
    def add_user(username: str, email: str, hashed_password: bytes,
                 is_active: str, is_admin: str) -> None:
        user = UserOrm(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
            is_admin=is_admin
        )

        try:
            with session_factory() as session:
                session.add_all([user])
                session.commit()
        except Exception as e:
            print(f"Error {e}")
            session.rollback()
            raise

