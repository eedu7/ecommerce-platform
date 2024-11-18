from fastapi import APIRouter, Depends

from app.controllers import AddressController
from app.models import User
from core.factory import Factory
from core.fastapi.dependencies import get_current_user

address_router: APIRouter = APIRouter()


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
    ...


@address_router.post(
    "/",
)
async def add_address():
    """
    Add a new address to the user
    """
    return {"message": "Adding a new address to the user"}


@address_router.get(
    "/{address_id}",
)
async def get_address_detail(address_id: str):
    """
    Retrieve the details of a saved address
    """
    return {"message": "Details of a specific address", "address_id": address_id}


@address_router.put(
    "/{address_id}",
)
async def update_address_detail(address_id: str):
    """
    Update the details of a saved address
    :param address_id:
    :return:
    """
    return {
        "message": "Updated details of a specific address",
        "address_id": address_id,
    }


@address_router.delete("/{address_id}")
async def delete_address_detail(address_id: str):
    """
    Delete a saved address
    :param address_id:
    :return:
    """
    return {
        "message": "Deleted details of a specific address",
        "address_id": address_id,
    }
