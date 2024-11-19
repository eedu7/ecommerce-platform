from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from app.controllers import AddressController
from app.models import Address, User
from app.schemas.requests.address import AddressRequest, AddressUpdateRequest
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
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a list of all saved addresses for the current user
    """
    user_id: int = current_user.id
    filters: Dict[str, Any] = {
        "user_id": user_id,
    }
    address: List[Address] = await address_controller.get_all(filters=filters)
    return address


@address_router.post(
    "/",
)
async def add_address(
    address_data: AddressRequest,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    """
    Add a new address to the user
    """
    address_data = address_data.model_dump(exclude_none=True)
    address_data["user_id"] = current_user.id
    new_address = await address_controller.create(address_data)
    return new_address


@address_router.get(
    "/{address_id}",
)
async def get_address_detail(
    address_id: UUID,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the details of a saved address
    """
    address: Address = await address_controller.get_by_uuid(address_id)
    if address.user_id != current_user.id:
        raise UnauthorizedException("Unauthorized")
    return address


@address_router.put(
    "/{address_id}",
)
@address_router.patch("/{address_id}")
async def update_address_detail(
    request: Request,
    address_id: UUID,
    address_data: AddressUpdateRequest,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    address = await address_controller.get_by_uuid(address_id)
    if address.user_id != current_user.id:
        raise UnauthorizedException("Unauthorized access")

    updated_data: Dict[str, Any] | None = None

    match request.method:
        case "PATCH":
            updated_data = address_data.model_dump(exclude_none=True)
        case "PUT":
            updated_data = address_data.model_dump()

    updated_address = await address_controller.update_model(address_id, updated_data)
    return updated_address


@address_router.delete("/{address_id}")
async def delete_address_detail(
    address_id: UUID,
    address_controller: AddressController = Depends(Factory().get_address_controller),
    current_user: User = Depends(get_current_user),
):
    address = await address_controller.get_by_uuid(address_id)
    if address.user_id != current_user.id:
        raise UnauthorizedException("Unauthorized")
    await address_controller.delete(address_id)
    return {
        "message": "Deleted details of a specific address",
    }
