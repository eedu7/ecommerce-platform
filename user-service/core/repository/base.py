from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.database import Base

# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD (Create, Read, Update, Delete) class for managing database operations
    on SQLAlchemy models asynchronously.

    This class provides common CRUD operations that can be inherited or instantiated
    for any SQLAlchemy model. All database operations are performed using an asynchronous
    session for non-blocking database access.
    """

    def __init__(self, model: Type[ModelType], db_session: AsyncSession) -> None:
        """
        Initialize the BaseRepository instance.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class to operate on.
            db_session (AsyncSession): An async database session.
        """
        self.session = db_session
        self.model = model

    async def create(self, attributes: Optional[Dict[str, Any]] = None) -> ModelType:
        """
        Create a new record in the database.

        Args:
            attributes (Optional[Dict[str, Any]]): A dictionary of attributes to set on the new record.

        Returns:
            ModelType: The created record instance.
        """
        if attributes is None:
            attributes = {}
        new_record = self.model(**attributes)
        self.session.add(new_record)
        return new_record

    async def get_all(
        self, skip: int = 0, limit: int = 20, filters: Optional[Dict[str, Any]] = None
    ) -> Sequence[ModelType]:
        """
        Retrieve a list of records with optional pagination and filtering.

        Args:
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to retrieve.
            filters (Optional[Dict[str, Any]]): Dictionary of field-value pairs to filter by.

        Returns:
            Sequence[ModelType]: A list of model instances.
        """
        query = select(self.model).offset(skip).limit(limit)
        if filters:
            query = query.filter_by(**filters)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_by(self, field: str, value: Any) -> Optional[ModelType]:
        """
        Retrieve a single record by a specific field and value.

        Args:
            field (str): The field name to filter by.
            value (Any): The value to filter on.

        Returns:
            Optional[ModelType]: The first model instance matching the criteria, or None.
        """
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(
        self, model: ModelType, attributes: Dict[str, Any]
    ) -> Optional[ModelType]:
        """
        Update an existing record with new attributes.

        Args:
            model (ModelType): The model instance to update.
            attributes (Dict[str, Any]): A dictionary of attributes to update.

        Returns:
            Optional[ModelType]: The updated model instance, or None if update failed.
        """
        for key, value in attributes.items():
            setattr(model, key, value)
        try:
            await self.session.flush()
            return model
        except SQLAlchemyError:
            await self.session.rollback()
            return None

    async def delete(self, model: ModelType) -> bool:
        """
        Delete a record.

        Args:
            model (ModelType): The model instance to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            await self.session.delete(model)
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False
