from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.controllers import AddressController
from app.models import Address, User
from app.schemas.requests.address import (AddressPartialUpdateRequest,
                                          AddressRequest, AddressUpdateRequest)
from core.exceptions import UnauthorizedException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

address_router: APIRouter = APIRouter(
    dependencies=[Depends(AuthenticationRequired)],
)


@address_router.get(
    "/",
)
async def get_address(
    skip: int = 0,
    limit: int = 20,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    return await address_controller.get_all_user_address(current_user.id, skip, limit)


@address_router.get(
    "/{address_id}",
)
async def get_address_detail(
    address_id: UUID,
    address_controller: AddressController = Depends(Factory().get_address_controller),
):
    """
    Retrieve the details of a saved address
    """
    address: Address = await address_controller.get_by_uuid(address_id)
    return address


@address_router.post(
    "/",
)
async def add_address(
    address_data: AddressRequest,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    return await address_controller.add_user_address(current_user.id, address_data)


@address_router.put("/{address_id}")
async def update_address_detail(
    address_id: UUID,
    address_data: AddressUpdateRequest,
    address_controller: AddressController = Depends(Factory().get_address_controller),
):
    return await address_controller.update_user_address(address_id, address_data)


@address_router.patch("/{address_id}")
async def update_address_detail(
    address_id: UUID,
    address_data: AddressPartialUpdateRequest,
    address_controller: AddressController = Depends(Factory().get_address_controller),
):
    return await address_controller.update_user_address(
        address_id, address_data, partial_update=True
    )


@address_router.delete("/{address_id}")
async def delete_address_detail(
    address_id: UUID,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    address = await address_controller.get_by_uuid(address_id)
    if address.user_id != current_user.id:
        raise UnauthorizedException(
            "Access denied: This address does not belong to the current user."
        )

    deleted: bool = await address_controller.delete(address_id)

    if deleted:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Address deleted"},
        )

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "Address deletion failed"},
    )
