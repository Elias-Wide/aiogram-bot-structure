from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    """
    A class for CRUD operations with users.

    This class provides methods for interacting with the `Users` model.
    """

    model = Users
