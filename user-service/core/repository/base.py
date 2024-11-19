from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD (Create, Read, Update, Delete) class for managing database operations
    on SQLAlchemy models asynchronously.

    This class provides common CRUD operations that can be inherited or instantiated
    for any SQLAlchemy model. All database operations are performed using an async
    session for asynchronous access.
    """

    def __init__(self, model: Type[ModelType], db_session: AsyncSession) -> None:
        """
        Initialize the BaseCRUD instance.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class to operate on.
            db_session (AsyncSession): An async database session.
        """
        self.session = db_session
        self.model: Type[ModelType] = model

    async def create(self, attributes: Optional[Dict[str, Any]] = None) -> ModelType:
        """
        Create a new record in the database
        :param attributes: (Dict[str, Any]) - A dictionary of attributes to assign to the new record.
        :return: ModelType: The created record.
        """
        attributes = attributes or {}
        model = self.model(**attributes)
        self.session.add(model)
        await self.session.flush()
        return model

    async def get_all(
        self, skip: int = 0, limit: int = 20, filters: Optional[Dict[str, Any]] = None
    ) -> Sequence[ModelType]:
        """
        Retrieve a list of all records, with optional pagination.

        Args:
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to retrieve.
            filters (Dict[str, Any], None):

        Returns:
            List[ModelType]: A list of model instances.
        """
        query = select(self.model).offset(skip).limit(limit)
        if filters:
            query = query.filter_by(**filters)
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by(self, field: str, value: Any) -> ModelType:
        """
        Retrieve a single record by a specified field and value.

        Args:
            field (str): The field name to filter by.
            value (Any): The value to filter the field with.

        Returns:
            ModelType: The first model instance matching the criteria.
        """
        query = select(self.model).where(
            getattr(self.model, field) == value
        )  # TODO: Adjust the types annotation
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, uuid: UUID) -> bool | None:
        """
        Delete a record by its unique ID.

        Args:
            uuid (str): The unique identifier of the record to delete.

        Returns:
            bool | None: True if deletion was successful, None if the record was not found.
        """
        model = await self.get_by(field="uuid", value=uuid)
        if model is None:
            return None
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def get_by_id(self, _id: str | int) -> ModelType:
        """
        Retrieve a single record by its unique ID.

        Args:
            _id (str): The unique identifier of the record.

        Returns:
            ModelType: The model instance with the specified ID.
        """
        _model = await self.get_by(field="id", value=_id)
        return _model

    async def update(self, _id: UUID, attributes: dict[str, Any]) -> ModelType | None:
        """
        Update an existing record by ID with specified attributes.

        Args:
            _id (UUID): The unique identifier of the record to update.
            attributes (dict[str, Any]): A dictionary of attributes to update on the model.

        Returns:
            ModelType | None: The updated model instance, or None if not found or attributes are None.
        """
        model = await self.get_by(field="uuid", value=_id)
        if model is None or attributes is None:
            return None

        for key, value in attributes.items():
            setattr(model, key, value)
        await self.session.flush()
        return model
