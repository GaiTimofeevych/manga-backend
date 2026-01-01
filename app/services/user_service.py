from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password  # Важно: verify_password здесь нужен

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    # 1. Проверяем, не занят ли email или username
    stmt = select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email или username уже существует"
        )

    # 2. Создаем модель пользователя
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role="user",
        is_active=True
    )
    
    # 3. Сохраняем в БД
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def authenticate_user(db: AsyncSession, identifier: str, password: str) -> User | None:
    """
    Аутентификация по Email ИЛИ по Username.
    identifier: может быть как email, так и username.
    """
    # Ищем пользователя, у которого email == identifier ИЛИ username == identifier
    stmt = select(User).where(
        or_(User.email == identifier, User.username == identifier)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    # Если юзера нет или пароль не подходит — возвращаем None
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
        
    return user