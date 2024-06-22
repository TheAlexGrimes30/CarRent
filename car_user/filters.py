from typing import Optional

from db.orm import SyncOrm


def filter_car_data(min_rent: Optional[int] = None,
                    max_rent: Optional[int] = None, drive_unit: Optional[str] = None,
                    min_year: Optional[int] = None, max_year: Optional[int] = None,
                    min_engine_power: Optional[int] = None, max_engine_power: Optional[int] = None,
                    transmission: Optional[str] = None, car_fuel: Optional[str] = None,
                    car_class: Optional[str] = None, car_brand: Optional[str] = None,
                    car_model: Optional[str] = None, car_status: Optional[str] = None):
    """
    Метод для валидации данных автомобиля для фильтрации
    :param min_rent:
    :param max_rent:
    :param drive_unit:
    :param min_year:
    :param max_year:
    :param min_engine_power:
    :param max_engine_power:
    :param transmission:
    :param car_fuel:
    :param car_class:
    :param car_brand:
    :param car_model:
    :param car_status:
    :return:
    """
    errors = {}
    car_brands = SyncOrm.get_all_brands()
    car_models = SyncOrm.get_all_models()

    if min_rent is not None:
        if min_rent <= 0:
            errors['min_rent'] = 'min rent must be greater than 0'

    if max_rent is not None:
        if max_rent <= 0:
            errors['max_rent'] = 'max rent must be greater than 0'
        elif min_rent is not None and min_rent > max_rent:
            errors['max_rent'] = 'max rent must not be less than min rent'

    if drive_unit is not None and drive_unit not in ['FWD', 'RWD', '4WD']:
        errors['drive_unit'] = 'Invalid drive unit data'

    if min_year is not None:
        if min_year <= 0:
            errors['min_year'] = 'min year must be greater than 0'
        elif max_year is not None and min_year > max_year:
            errors['min_year'] = 'min year must not be greater than max year'

    if max_year is not None and max_year <= 0:
        errors['max_year'] = 'max year must be greater than 0'

    if min_engine_power is not None:
        if min_engine_power <= 0:
            errors['min_engine_power'] = 'min engine power must be greater than 0'
        elif max_engine_power is not None and min_engine_power > max_engine_power:
            errors['min_engine_power'] = 'min engine power must not be greater than max engine power'

    if max_engine_power is not None and max_engine_power <= 0:
        errors['max_engine_power'] = 'max engine power must be greater than 0'

    if transmission is not None and transmission not in ['АКПП', 'МКПП', 'Вариатор', 'Робот']:
        errors['transmission'] = 'Invalid transmission data'

    if car_class is not None and car_class not in ['A', 'B', 'C', 'D', 'E', 'F', 'M', 'S', 'J', 'truck', 'van']:
        errors['car_class'] = 'Invalid car class data'

    if car_fuel is not None and car_fuel not in ['дизель', 'бензин', 'гибрид', 'электро', 'водород']:
        errors['car_fuel'] = 'Invalid car fuel data'

    if car_status is not None and car_status not in ['0', '1']:
        errors['car_status'] = 'Invalid car status data'

    if car_brand is not None and len(car_brands) != 0 and car_brand not in car_brands:
        errors['car_brand'] = 'Invalid car brand data'

    if len(car_brands) == 0:
        errors['car_brand'] = 'There are not car brands in database'

    if len(car_models) == 0:
        errors['car_model'] = 'There are not car models in database'

    if car_model is not None and len(car_models) != 0 and car_model not in car_models:
        errors['car_model'] = 'Invalid car model data'

    return errors if errors else None
