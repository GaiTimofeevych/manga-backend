from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    Получить профиль текущего пользователя.
    Требует JWT токен в заголовке Authorization.
    """
    return current_user