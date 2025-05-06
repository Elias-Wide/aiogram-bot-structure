"""Модуль с функциями анкеты."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    Message,
)

from app.bot.filters import UserExistFilter
from app.users.dao import UsersDAO


registration_router = Router()
registration_router.message.filter(~UserExistFilter())


@registration_router.message(default_state, CommandStart())
async def begin_registration(
    message: Message,
    state: FSMContext,
) -> None:
    pass
