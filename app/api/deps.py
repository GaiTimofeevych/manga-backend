from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.token import TokenData
from app.services.user_service import select # Нам понадобится простой select

# Эта штука говорит Swagger UI, что для входа нужно отправить токен 
# на адрес /api/v1/auth/login
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login" if hasattr(settings, "API_V1_STR") else "/api/v1/auth/login"
)

async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth2)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Эта функция:
    1. Достает токен из заголовка Authorization.
    2. Расшифровывает его.
    3. Ищет юзера в БД по ID из токена.
    4. Если что-то не так — кидает ошибку 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Расшифровываем токен
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Сохраняем данные во временную схему
        token_data = TokenData(username=user_id) # В поле username у нас лежит ID (так уж вышло в Pydantic схеме)
        
    except (JWTError, ValidationError):
        raise credentials_exception

    # Ищем пользователя в базе
    # Нам нужно сделать простой запрос по ID. 
    # Т.к. в user_service у нас нет метода get_by_id, напишем запрос прямо тут или добавим в сервис.
    # Для чистоты архитектуры лучше делать через сервис, но пока сделаем прямой запрос для наглядности.
    user = await db.get(User, token_data.username) # .get ищет по Primary Key (UUID)
    
    if user is None:
        raise credentials_exception
        
    return user

# Вспомогательная зависимость: только для активных юзеров
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user