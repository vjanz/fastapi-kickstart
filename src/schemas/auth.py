from uuid import UUID

from pydantic import EmailStr, Field

from src.schemas.base import BaseSchema


class UserLoginResponse(BaseSchema):
    access_token: str
    token_type: str


class UserBase(BaseSchema):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: UUID


class UserSignUpResponse(BaseSchema):
    message: str
    user_id: str
