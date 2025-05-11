from datetime import datetime
from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import Base, async_session_maker
from app.core.logging import logger


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base Data Access Object (DAO) class for database operations.

    This class provides generic methods for CRUD operations on database models.
    """

    model = None

    @classmethod
    async def get_by_id(
        cls,
        obj_id: int,
    ) -> ModelType | None:
        """
        Retrieve an object by its ID.

        Args:
            obj_id (int): The ID of the object to retrieve.

        Returns:
            ModelType | None: The retrieved object or None if not found.
        """
        async with async_session_maker() as session:
            db_obj = await session.execute(
                select(cls.model).where(cls.model.id == obj_id),
            )
            return db_obj.scalars().first()

    @classmethod
    async def get_multi(cls):
        """
        Retrieve all objects of the model.

        Returns:
            list[ModelType]: A list of all objects.
        """
        async with async_session_maker() as session:
            db_objs = await session.execute(select(cls.model))
            return db_objs.scalars().all()

    @classmethod
    async def create(
        cls,
        data: dict,
    ) -> ModelType:
        """
        Create a new object in the database.

        Args:
            data (dict): The data to create the object with.

        Returns:
            ModelType: The created object.
        """
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                object = await session.execute(query)
                await session.commit()
                return object.mappings().first()
            except (SQLAlchemyError, Exception) as error:
                await session.rollback()
                if isinstance(error, SQLAlchemyError):
                    message = "Database Exception"
                elif isinstance(error, Exception):
                    message = "Unknown Exception"
                message += ": Unable to add data."
                logger.error(message)
                raise error

    @classmethod
    async def update(
        cls,
        db_obj: ModelType,
        new_data: UpdateSchemaType,
    ) -> ModelType:
        """
        Update an existing object in the database.

        Args:
            db_obj (ModelType): The object to update.
            new_data (UpdateSchemaType): The new data to update the object with.

        Returns:
            ModelType: The updated object.
        """
        async with async_session_maker() as session:
            try:
                obj_data = jsonable_encoder(db_obj)
                for field in obj_data:
                    if field in new_data:
                        setattr(db_obj, field, new_data[field])
                session.add(db_obj)
                await session.commit()
                await session.refresh(db_obj)
                return db_obj
            except Exception as error:
                logger.error(error)
                await session.rollback()
                raise error

    @classmethod
    async def delete_object(cls, **kwargs):
        """
        Delete an object from the database.

        Args:
            **kwargs: The filter criteria to find the object to delete.

        Returns:
            ModelType | None: The deleted object or None if not found.
        """
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar()
                object_to_delete = result
                if not result:
                    return None
                await session.delete(result)
                await session.commit()
                return object_to_delete
            except Exception as error:
                logger.error(error)
                return None

    @classmethod
    async def get_by_attribute(
        cls,
        attr_name: str,
        attr_value: str,
    ) -> ModelType | None:
        """
        Retrieve an object by a specific attribute.

        Args:
            attr_name (str): The name of the attribute.
            attr_value (str): The value of the attribute.

        Returns:
            ModelType | None: The retrieved object or None if not found.
        """
        async with async_session_maker() as session:
            db_obj = await session.execute(
                select(cls.model).where(
                    getattr(cls.model, attr_name) == attr_value,
                ),
            )
            return db_obj.scalars().first()
