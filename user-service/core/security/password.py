from passlib.context import CryptContext


class PasswordHandler:
    pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @staticmethod
    def hash(password: str) -> str:
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, password: str) -> bool:
        return PasswordHandler.pwd_context.verify(password, hashed_password)
