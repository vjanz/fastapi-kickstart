import logging

from sqlalchemy.orm import Session

from src.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from src.core.security import create_access_token, pwd_context
from src.models import User
from src.repositories.user import UserRepository
from src.schemas.auth import UserCreate

logger = logging.getLogger(__name__)


class HashingMixin:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


class AuthService(HashingMixin):
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def signup(self, user: UserCreate) -> User:
        logger.info(f"Attempting signup for user: {user.email}")
        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsException()

        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=self.hash_password(user.password),
        )
        return self.user_repository.create(new_user)

    def authenticate(self, email: str, password: str) -> str:
        logger.info(f"User login attempt: {email}")
        user = self.user_repository.get_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            raise InvalidCredentialsException()
        access_token = create_access_token(data={"sub": user.email})
        return access_token
