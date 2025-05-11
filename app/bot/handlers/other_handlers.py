"""This module contains handlers for unsupported commands and banned users."""

from aiogram import Router
from aiogram.types import Message

from app.bot.filters import BanFilter
from app.core.config import settings

echo_router = Router()
ban_router = Router()
ban_router.message.filter(~BanFilter())


@echo_router.message()
async def send_echo(message: Message) -> None:
    """
    Sends a reply when an unsupported command is received.

    Args:
        message (Message): The message object containing the unsupported command.
    """
    await message.reply(
        f"Currently, I do not support the command {message.text} 🤷\n\n"
        f"You can contact @{settings.telegram.admin_username} with suggestions "
        "to improve the bot or to report a bug."
    )


@ban_router.message()
async def send_banned_message(message: Message) -> None:
    """
    Sends a reply to a banned user.

    Args:
        message (Message): The message object from the banned user.
    """
    await message.reply("You are banned from accessing this bot.")
