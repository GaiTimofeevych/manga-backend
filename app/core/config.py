from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field
from typing import Optional

class Settings(BaseSettings):
    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    REDIS_URL: str = "redis://localhost:6379"

    # Секретный ключ для JWT токенов (сгенерируем позже, пока заглушка)
    SECRET_KEY: str = "super-secret-key-change-me-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        extra="ignore" # Игнорировать лишние переменные в .env
    )

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Собираем строку подключения: postgresql+asyncpg://user:pass@host:port/db
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"{self.POSTGRES_DB}",
        ))

settings = Settings()