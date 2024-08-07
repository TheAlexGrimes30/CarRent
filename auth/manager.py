from typing import Optional

from fastapi_users import IntegerIDMixin, BaseUserManager, schemas, models, exceptions

from auth.utils import SECRET_KEY
from db.database import get_user_db
from db.models import UserOrm
from fastapi import Request, Depends


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):
    """
    Класс для работы с данными пользователя при авторизации
    """
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: UserOrm, request: Optional[Request] = None):
        """
        Вывод сообщения после регистрации пользователя
        :param user:
        :param request:
        :return:
        """
        print(f"User {user.id} has registered.")

    async def validate_password(self, password: str, user: schemas.UC) -> None:
        """
        Валидация пароля
        :param password:
        :param user:
        :return:
        """
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(reason="Password must be at least 8 characters long.")
        await super().validate_password(password, user)

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Регистрация пользователя
        :param user_create:
        :param safe:
        :param request:
        :return:
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password).encode("utf-8")

        user_dict["is_superuser"] = user_create.is_superuser

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
