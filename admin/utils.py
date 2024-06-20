import re
from datetime import datetime
from typing import Optional


def validate_data_image(filename):
    """
    Валидация изображения автомобиля
    :param filename:
    :return:
    """
    image_extensions_pattern = r'\.(jpg|jpeg|png|gif|bmp)$'
    if isinstance(filename, str) and re.search(image_extensions_pattern, filename, re.IGNORECASE):
        return True
    else:
        return False


def validate_car_number(car_number):
    """
    Валидация номера автомобиля
    :param car_number: Номер автомобиля
    :return: True если номер валиден, иначе False
    """
    car_number_pattern = r'^[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$'
    if isinstance(car_number, str) and re.match(car_number_pattern, car_number, re.IGNORECASE):
        return True
    else:
        return False


def validate_car_data(rent_deposit: Optional[int], car_fuel: Optional[str], car_year: Optional[int],
                      transmission: Optional[str], car_status: Optional[str], drive_unit: Optional[str],
                      car_class: Optional[str], car_photo: Optional[str], car_number: Optional[str]) -> Optional[dict]:
    """
    Валидация данных автомобиля
    :param car_number:
    :param rent_deposit:
    :param car_fuel:
    :param car_year:
    :param transmission:
    :param car_status:
    :param drive_unit:
    :param car_class:
    :param car_photo:
    :return:
    """
    errors = {}

    if rent_deposit is not None and rent_deposit <= 0:
        errors['rent_deposit'] = 'Rent Deposit must be greater than 0'

    if car_fuel is not None and car_fuel not in ['дизель', 'бензин', 'гибрид', 'электро', 'водород']:
        errors['car_fuel'] = 'Invalid fuel type'

    if car_year is not None and (car_year < 1970 or car_year > datetime.now().year):
        errors['car_year'] = 'Invalid year'

    if transmission is not None and transmission not in ['АКПП', 'МКПП', 'Вариатор', 'Робот']:
        errors['transmission'] = 'Invalid transmission'

    if car_status is not None and car_status not in ['0', '1']:
        errors['car_status'] = 'Invalid status of car'

    if drive_unit is not None and drive_unit not in ['FWD', 'RWD', '4WD']:
        errors['drive_unit'] = 'Invalid drive unit'

    if car_class is not None and car_class not in ['A', 'B', 'C', 'D', 'E', 'F', 'M', 'S', 'J', 'truck', 'van']:
        errors['car_class'] = 'Invalid car class'

    if car_photo is not None and not validate_data_image(car_photo):
        errors['car_photo'] = 'Invalid image data'

    if car_number is not None and not validate_car_number(car_number):
        errors['car_number'] = 'Invalid car number'

    return errors if errors else None
