from fastapi import HTTPException

from src.core.error_messages import AuthErrorMessages


class UserAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail=AuthErrorMessages.EMAIL_REGISTERED)


class InvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail=AuthErrorMessages.INVALID_CREDENTIALS)
