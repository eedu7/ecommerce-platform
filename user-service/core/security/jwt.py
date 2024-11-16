from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import ExpiredSignatureError, JWTError, jwt

from core.config import config
from core.exceptions import UnauthorizedException


class JWTDecodeError(UnauthorizedException):
    def __init__(self, message="Invalid token"):
        super().__init__(message)


class JWTExpiredError(UnauthorizedException):
    def __init__(self, message="Token expired"):
        super().__init__(message)


class JWTHandler:
    SECRET_KEY: str = config.JWT_SECRET_KEY
    ALGORITHM: str = config.JWT_ALGORITHM
    expire_minutes: int = config.JWT_EXPIRE_MINUTES

    @staticmethod
    def encode(payload: Dict[str, Any]) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=JWTHandler.expire_minutes
        )
        payload.update({"exp": expire})
        return jwt.encode(
            payload,
            JWTHandler.SECRET_KEY,
            algorithm=JWTHandler.ALGORITHM,
        )

    @staticmethod
    def decode(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                JWTHandler.SECRET_KEY,
                algorithms=[JWTHandler.ALGORITHM],
            )
        except ExpiredSignatureError as exception:
            raise JWTExpiredError() from exception
        except JWTError as exception:
            raise JWTDecodeError() from exception

    @staticmethod
    def decode_expire(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                JWTHandler.SECRET_KEY,
                algorithms=[JWTHandler.ALGORITHM],
                options={"verify_exp": False},
            )
        except JWTError as exception:
            raise JWTDecodeError() from exception
