from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions import UnauthorizedException


class AuthenticationRequiredException(UnauthorizedException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message)


class AuthenticationRequired:
    def __init__(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        if not token:
            raise AuthenticationRequiredException("Authentication required")
