import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# 1. Фикстура: Движок БД (создается для каждого теста заново)
@pytest.fixture(scope="function")
async def engine():
    # Создаем движок
    eng = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    
    # Создаем таблицы
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield eng
    
    # Удаляем таблицы после теста (чтобы очистить данные)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await eng.dispose()

# 2. Фикстура: Сессия БД
@pytest.fixture(scope="function")
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    async with async_session_factory() as session:
        yield session
        # На всякий случай делаем откат
        await session.rollback()

# 3. Фикстура: Клиент
@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()