from typing import Any, Dict, Sequence
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse

from app.models import Address
from app.repositories import AddressRepository
from app.schemas.requests.address import (AddressPartialUpdateRequest,
                                          AddressRequest, AddressUpdateRequest)
from core.controller import BaseController
from core.exceptions import BadRequestException


class AddressController(BaseController[Address]):
    def __init__(self, address_repository: AddressRepository):
        super().__init__(model=Address, repository=address_repository)
        self.address_repository = address_repository

    async def get_all_user_address(
        self, user_id: int, skip: int, limit: int
    ) -> Sequence[Address]:
        filters: Dict[str, int] = {"user_id": user_id}
        try:
            addresses: Sequence[Address] = await self.address_repository.get_all(
                skip=skip, limit=limit, filters=filters
            )
            return addresses
        except Exception as e:
            raise BadRequestException(f"Error getting all user addresses. {e}")

    async def add_user_address(self, user_id: int, address: AddressRequest) -> Address:
        data: Dict[str, Any] = address.model_dump()
        data.update(
            {
                "user_id": user_id,
                "created_by": user_id,
                "updated_by": user_id,
            }
        )
        try:
            new_address: Address = await self.address_repository.create(data)
            return new_address
        except Exception as e:
            raise BadRequestException(f"Error adding user address. {e}")

    async def update_user_address(
        self,
        address_uuid: UUID,
        address: AddressUpdateRequest | AddressPartialUpdateRequest,
        partial_update: bool = False,
    ) -> Address:
        if partial_update:
            data: Dict[str, Any] = address.model_dump(exclude_none=True)
        else:
            data: Dict[str, Any] = address.model_dump()

        try:
            updated_address: Address = await self.address_repository.update(
                address_uuid, data
            )
            return updated_address
        except Exception as e:
            raise BadRequestException(f"Error updating user address. {e}")

    async def delete_user_address(self, address_uuid: UUID) -> JSONResponse:
        try:
            deleted: bool = await self.repository.delete(address_uuid)
            if deleted:
                return JSONResponse(
                    status_code=status.HTTP_204_NO_CONTENT,
                    content={"message": "User address deleted"},
                )
            raise BadRequestException(f"Error deleting user address. {deleted}")
        except Exception as e:
            raise BadRequestException(f"Error deleting user address. {e}")
