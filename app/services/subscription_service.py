from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subscription import Subscription

async def check_subscription(db: AsyncSession, user_id: str) -> bool:
    """
    Проверяет, есть ли у пользователя активная подписка.
    Возвращает True, если есть подписка и она еще не истекла.
    """
    now = datetime.now(timezone.utc)
    
    # Ищем подписку этого юзера, у которой дата окончания БОЛЬШЕ, чем сейчас
    stmt = select(Subscription).where(
        Subscription.user_id == user_id,
        Subscription.end_date > now
    )
    result = await db.execute(stmt)
    subscription = result.scalar_one_or_none()
    
    return subscription is not None

async def grant_subscription(db: AsyncSession, user_id: str, days: int = 30) -> Subscription:
    """
    Выдать подписку пользователю на N дней.
    """
    now = datetime.now(timezone.utc)
    end_date = now + timedelta(days=days)
    
    new_sub = Subscription(
        user_id=user_id,
        plan_type="premium",
        start_date=now,
        end_date=end_date
    )
    
    db.add(new_sub)
    await db.commit()
    await db.refresh(new_sub)
    return new_sub