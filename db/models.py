from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, CheckConstraint, Integer, Column, LargeBinary, Boolean
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

Base = declarative_base()


class CarsOrm(Base):
    """
    Модель таблицы, содержащая данные автомобиля
    """
    __tablename__ = "cars"
    __table_args__ = (
        CheckConstraint('rent_deposit > 0'),
        CheckConstraint("car_class in ('A', 'B', 'C', 'D', 'E', 'F', 'M', 'S', 'J', 'truck', 'van')"),
        CheckConstraint("car_fuel in ('дизель', 'бензин', 'гибрид', 'электро', 'водород')"),
        CheckConstraint("drive_unit in ('FWD', 'RWD', '4WD')"),
        CheckConstraint("transmission in ('АКПП', 'МКПП', 'Вариатор', 'Робот')"),
        CheckConstraint("car_status in ('0', '1')"),
        CheckConstraint("car_year > 1970")
    )

    car_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_brand: Mapped[str] = mapped_column(String(64), nullable=False)
    car_model: Mapped[str] = mapped_column(String(64), nullable=False)
    rent_deposit: Mapped[int] = mapped_column(Integer, nullable=False)
    car_class: Mapped[str] = mapped_column(String(32), nullable=False)
    drive_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    car_fuel: Mapped[str] = mapped_column(String(32), nullable=False)
    car_year: Mapped[int] = mapped_column(Integer, nullable=False)
    engine_power: Mapped[int] = mapped_column(Integer, nullable=False)
    transmission: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    car_number: Mapped[str] = mapped_column(String(64), nullable=False)
    car_photo: Mapped[str] = mapped_column(String(256), nullable=False)
    car_status: Mapped[str] = mapped_column(String, nullable=False)


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель таблицы, содержащая данные пользователя
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
