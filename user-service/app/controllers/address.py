from app.models import Address
from app.repositories import AddressRepository
from core.controller import BaseController


class AddressController(BaseController[Address]):
    def __init__(self, address_repository: AddressRepository):
        super().__init__(model=Address, repository=address_repository)
        self.address_repository = address_repository
