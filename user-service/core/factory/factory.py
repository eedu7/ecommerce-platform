from functools import partial

from fastapi import Depends

from app.controllers import AuthController, UserController, AddressController
from app.models import User, Address
from app.repositories import UserRepository, AddressRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    address_repositryo = partial(AddressRepository, Address)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )

    def get_address_controller(self, db_session=Depends(get_session)):
        return AddressController(
            address_repository=self.address_repositryo(db_session=db_session)
        )