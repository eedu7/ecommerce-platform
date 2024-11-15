from functools import reduce
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.session = db_session
        self.model_class: Type[ModelType] = model

    async def create(self, attributes: Optional[dict[str, Any]] = None) -> ModelType:
        """
        Creates the model instance.
        """
        attributes = attributes or {}
        model = self.model_class(**attributes)
        self.session.add(model)
        await self.session.flush()  # Ensures the object gets an ID
        return model

    async def get_all(
        self, skip: int = 0, limit: int = 100, join_: Optional[set[str]] = None
    ) -> list[ModelType]:
        """
        Returns a list of model instances.
        """
        query = self._query(join_)
        query = query.offset(skip).limit(limit)
        return await self._all(query)

    async def get_by(
        self,
        field: str,
        value: Any,
        join_: Optional[set[str]] = None,
        unique: bool = False,
    ) -> Optional[ModelType]:
        """
        Returns the model instance matching the field and value.
        """
        query = self._query(join_)
        query = self._get_by(query, field, value)

        if unique:
            return await self._one_or_none(query)

        return await self._all(query)

    async def delete(self, model: ModelType) -> None:
        """
        Deletes the model instance.
        """
        await self.session.delete(model)

    def _query(
        self, join_: Optional[set[str]] = None, order_: Optional[dict] = None
    ) -> Select:
        """
        Builds a query for the model.
        """
        query = select(self.model_class)
        query = self._maybe_join(query, join_)
        query = self._maybe_ordered(query, order_)
        return query

    async def _all(self, query: Select) -> list[ModelType]:
        """
        Executes the query and returns all results.
        """
        result = await self.session.scalars(query)
        return result.all()

    async def _one_or_none(self, query: Select) -> Optional[ModelType]:
        """
        Executes the query and returns one or None.
        """
        result = await self.session.scalars(query)
        return result.one_or_none()

    def _get_by(self, query: Select, field: str, value: Any) -> Select:
        """
        Filters the query by a field and value.
        """
        if not hasattr(self.model_class, field):
            raise ValueError(f"Invalid field: {field}")
        return query.where(getattr(self.model_class, field) == value)

    def _maybe_join(self, query: Select, join_: Optional[set[str]]) -> Select:
        """
        Adds joins to the query if specified.
        """
        if not join_:
            return query
        if not isinstance(join_, set):
            raise TypeError("join_ must be a set")
        return reduce(self._add_join_to_query, join_, query)

    def _maybe_ordered(self, query: Select, order_: Optional[dict]) -> Select:
        """
        Adds ordering to the query if specified.
        """
        if not order_:
            return query
        for order_type, fields in order_.items():
            if order_type not in {"asc", "desc"}:
                raise ValueError("Invalid order type: must be 'asc' or 'desc'")
            for field in fields:
                if not hasattr(self.model_class, field):
                    raise ValueError(f"Invalid order field: {field}")
                column = getattr(self.model_class, field)
                query = query.order_by(
                    column.asc() if order_type == "asc" else column.desc()
                )
        return query

    def _add_join_to_query(self, query: Select, join_: str) -> Select:
        """
        Adds a join to the query.
        """
        join_method = getattr(self, f"_join_{join_}", None)
        if not callable(join_method):
            raise AttributeError(f"No join method for: {join_}")
        return join_method(query)
