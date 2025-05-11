from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """
    Parent class for the base model.

    This class provides a default implementation for table naming and
    includes a primary key column.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Returns the table name in lowercase.

        The table name is derived from the class name and converted to lowercase.
        """
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


# Create an asynchronous database engine using the database URL from settings
engine = create_async_engine(settings.db.url)

# Create a session maker for asynchronous database sessions
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase, PreBase):
    """
    Base class for all database models.

    Combines SQLAlchemy's DeclarativeBase with the PreBase class to provide
    default table naming and a primary key column.
    """

    pass
