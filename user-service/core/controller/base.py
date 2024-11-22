from typing import Any, Dict, Generic, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from core.database import Base, Propagation, Transactional
from core.exceptions import NotFoundException
from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: Type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_id(self, id_: int) -> ModelType:
        """
        Returns the model instance matching the id.

        :param id_: The id to match.
        :return: The model instance.
        """

        db_obj = await self.repository.get_by(field="id", value=id_)
        return db_obj

    async def get_by_uuid(self, uuid: UUID) -> ModelType | None:
        """
        Returns the model instance matching the uuid.

        :param uuid: The uuid to match.
        :return: The model instance.
        """

        db_obj = await self.repository.get_by(field="uuid", value=uuid)
        return db_obj

    async def get_all(
        self, skip: int = 0, limit: int = 100, filters: Dict[str, Any] | None = None
    ) -> list[ModelType]:
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param filters: The filters to apply to the query.
        :return: A list of records.
        """

        response = await self.repository.get_all(skip, limit, filters)
        return response

    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """
        Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.
        :return: The created object.
        """
        create = await self.repository.create(attributes)
        return create

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(self, model: ModelType) -> bool:
        delete = await self.repository.delete(model)
        return delete

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_model(
        self, model: ModelType, attributes: dict[str, Any]
    ) -> ModelType:
        updated = await self.repository.update(model, attributes)
        return updated
