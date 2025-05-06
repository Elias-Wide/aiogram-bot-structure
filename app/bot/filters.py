"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.core.config import settings


from app.users.dao import UsersDAO

from app.core.logging import logger


class UserExistFilter(BaseFilter):
    """
    Класс фильтрации пользователя по telegram_id.
    Возвращает True для зарегистрированного пользователя.
    """

    def __init__(self) -> None:
        self.modelDAO = UsersDAO
        self.attr_name = "telegram_id"

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        if self.attr_name == "telegram_id":
            attr_value = message.from_user.id
        else:
            attr_value = int(message.text)
        obj = await self.modelDAO.get_by_attribute(
            attr_name=self.attr_name, attr_value=attr_value
        )
        if obj:
            return {self.attr_name: attr_value, "model_obj": obj}
        logger(False)
        return False


class BanFilter(UserExistFilter):
    """Класс фильтрации по наличию бана у пользователя."""

    async def __call__(self, message: Message):
        """
        Проверить пользователя на наличие бана.
        Делает базовую проверку на регистрацию из родительского класса
        и проверяет на наличие бана.
        """
        user = await super().__call__(message)
        if user and user["model_obj"].ban == True:
            return False
        return user


class AdminFilter(BaseFilter):
    """Класс фильтрации по наличию прав админа."""

    async def __call__(self, message: Message):
        if message.from_user.id == int(settings.telegram.admin_id):
            return True
        return False
