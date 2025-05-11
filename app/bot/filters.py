"""Filters for handling user-related checks in the bot."""

from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.core.config import settings
from app.users.dao import UsersDAO


class UserExistFilter(BaseFilter):
    """
    Filter class to check if a user exists based on their Telegram ID.

    Returns True for a registered user.
    """

    def __init__(self) -> None:
        self.modelDAO = UsersDAO
        self.attr_name = "telegram_id"

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        """
        Check if the user exists in the database.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the user exists, otherwise False.
        """
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
    """
    Filter class to check if a user is banned.

    Inherits from UserExistFilter to perform a basic registration check
    and adds a ban status check.
    """

    async def __call__(self, message: Message):
        """
        Check if the user is banned.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: False if the user is banned, otherwise the user object.
        """
        user = await super().__call__(message)
        if user and user["model_obj"].ban is True:
            return False
        return user


class AdminFilter(BaseFilter):
    """
    Filter class to check if the user has admin rights.

    Returns True if the user is the admin.
    """

    async def __call__(self, message: Message):
        """
        Check if the user is the admin.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the user is the admin, otherwise False.
        """
        if message.from_user.id == int(settings.telegram.admin_id):
            return True
        return False
