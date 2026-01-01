from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. Создаем движок (Engine)
# echo=True будет выводить все SQL запросы в консоль (полезно для отладки, в проде отключают)
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

# 2. Создаем фабрику сессий
# expire_on_commit=False обязателен для асинхронной работы
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# 4. Dependency (Зависимость) для FastAPI
# Эта функция будет выдавать новую сессию для каждого запроса и закрывать её после
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()