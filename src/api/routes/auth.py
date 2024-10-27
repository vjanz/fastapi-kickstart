from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies import get_auth_service
from src.schemas.auth import UserCreate, UserLoginResponse, UserSignUpResponse
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserSignUpResponse)
def signup(
    user: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    new_user = auth_service.signup(user)
    return {"message": "User created successfully", "user_id": str(new_user.id)}


@router.post("/login", response_model=UserLoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    access_token = auth_service.authenticate(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}
