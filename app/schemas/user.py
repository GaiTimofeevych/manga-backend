import uuid
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# Базовая схема (общие поля)
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Схема для РЕГИСТРАЦИИ (клиент присылает пароль)
class UserCreate(UserBase):
    password: str

# Схема для ОТВЕТА (мы НЕ возвращаем пароль, но возвращаем ID и дату)
class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    # Эта настройка нужна, чтобы Pydantic мог читать данные прямо из SQLAlchemy моделей
    model_config = ConfigDict(from_attributes=True)