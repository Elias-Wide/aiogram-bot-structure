from datetime import datetime
from sqlalchemy import and_, any_, insert, or_, select
from sqlalchemy.orm import aliased

from app.core.logging import logger
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    """Класс CRUD-операций с пользователями."""

    model = Users
