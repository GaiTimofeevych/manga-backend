from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.models.user import User
from app.api.deps import get_current_active_user
from app.services import subscription_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

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



@router.post("/subscribe", status_code=201)
async def subscribe_test(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Тестовый эндпоинт: Выдать себе подписку.
    В реальной жизни здесь была бы интеграция со Stripe.
    """
    return await subscription_service.grant_subscription(db, user_id=current_user.id, days=days)