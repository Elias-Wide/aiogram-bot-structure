from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):

    level: int = 0
    menu_name: str
    user_id: int | None = None
