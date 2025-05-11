from aiogram import Router

from app.bot.filters import BanFilter

from app.bot.handlers.other_handlers import echo_router


main_router = Router()
main_router.message.filter(BanFilter())

main_router.include_routers(echo_router)
