from typing import Any, Dict, Optional, Sequence
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse

from app.models import Address
from app.repositories import AddressRepository
from app.schemas.requests.address import (AddressPartialUpdateRequest,
                                          AddressRequest, AddressUpdateRequest)
from core.controller import BaseController
from core.exceptions import BadRequestException, NotFoundException


class AddressController(BaseController[Address]):
    def __init__(self, address_repository: AddressRepository):
        super().__init__(model=Address, repository=address_repository)

        self.address_repository = address_repository

    async def get_by_user_address(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> Sequence[Address]:
        try:
            return await self.address_repository.get_by_user_address(
                user_id, skip=skip, limit=limit
            )
        except Exception as e:
            raise BadRequestException(f"Error getting address. {e}")

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
            return await self.create(data)
        except Exception as e:
            raise BadRequestException(f"Error adding user address. {e}")

    async def update_user_address(
        self,
        address_uuid: UUID,
        address_data: AddressUpdateRequest | AddressPartialUpdateRequest,
        partial_update: bool = False,
    ) -> Address:
        address: Address | None = await self.get_by_uuid(address_uuid)

        if not address:
            raise NotFoundException(f"Address {address_uuid} not found")

        if partial_update:
            address_data: Dict[str, Any] = address_data.model_dump(exclude_none=True)
        else:
            address_data: Dict[str, Any] = address_data.model_dump()

        try:
            updated_address: Address = await self.update_model(address, address_data)
            return updated_address
        except Exception as e:
            raise BadRequestException(f"Error updating user address. {e}")

    async def delete_user_address(self, address_uuid: UUID) -> JSONResponse:
        """
        Delete a user's address by UUID.

        Args:
            address_uuid (UUID): UUID of the address to delete.

        Returns:
            JSONResponse: HTTP response indicating success or failure.
        """
        address: Optional[Address] = await self.get_by_uuid(address_uuid)
        if not address:
            raise NotFoundException(f"Address {address_uuid} not found")
        try:
            await self.delete(address)
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={"message": "User address deleted"},
            )
        except Exception as e:
            raise BadRequestException(f"Error deleting user address: {e}")
