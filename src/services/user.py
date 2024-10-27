from src.models import User
from src.repositories.user import UserRepository
from src.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository
