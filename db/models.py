from typing import Annotated

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

id = Annotated[int, mapped_column(primary_key=True)]
car_brand = Annotated[str, mapped_column(String(64), nullable=False)]
car_model = Annotated[str, mapped_column(String(64), nullable=False)]
rent_deposit = Annotated[int, mapped_column(nullable=False)]
car_class = Annotated[str, mapped_column(String(32), nullable=False)]
drive_unit = Annotated[str, mapped_column(String(32), nullable=False)]
car_fuel = Annotated[str, mapped_column(String(32), nullable=False)]
car_year = Annotated[int, mapped_column(nullable=False)]
engine_power = Annotated[int, mapped_column(nullable=False)]
transmission = Annotated[str, mapped_column(nullable=False)]
description = Annotated[str, mapped_column(nullable=False)]
car_number = Annotated[str, mapped_column(String(64), nullable=False)]
car_photo = Annotated[str, mapped_column(String(256), nullable=False)]
car_status = Annotated[str, mapped_column(nullable=False)]


class Base(DeclarativeBase):
    pass


class CarsOrm(Base):
    """
    Модель таблицы, содержащая данные автомобиля
    """
    __tablename__ = "cars"
    __table_args__ = (
        CheckConstraint('car_price > 0'),
        CheckConstraint("car_class in ('A', 'B', 'C', 'D', 'E', 'F', 'M', 'S', 'J')"),
        CheckConstraint("car_fuel in ('дизель', 'бензин', 'гибрид', 'электро', 'водород')"),
        CheckConstraint("transmission in ('АКПП', 'МКПП', 'Вариатор', 'Робот')"),
        CheckConstraint("rent_deposit > 0"),
        CheckConstraint("car_status in ('0', '1')"),
        CheckConstraint("car_year > 1970")
    )
    id = Mapped[id]
    car_brand = Mapped[car_brand]
    car_model = Mapped[car_status]
    rent_deposit = Mapped[rent_deposit]
    car_class = Mapped[car_class]
    drive_unit = Mapped[drive_unit]
    car_fuel = Mapped[car_fuel]
    car_year = Mapped[car_year]
    engine_power = Mapped[engine_power]
    transmission = Mapped[transmission]
    description = Mapped[description]
    car_number = Mapped[car_number]
    car_photo = Mapped[car_photo]
    car_status = Mapped[car_status]

