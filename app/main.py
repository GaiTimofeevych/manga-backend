from fastapi.staticfiles import StaticFiles
import os
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.database import engine
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.core.config import settings
# Импортируем наш новый роутер
from app.api.v1.endpoints import auth, users, manga, utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")

     # 1. Подключаемся к Redis
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="manga-cache")
    print("✅ Redis cache initialized")
    
    # Тут можно добавить проверку БД, если хочешь, как было раньше
    yield
    print("🛑 Shutting down...")
    await engine.dispose()
    await redis.close() # Закрываем соединение

app = FastAPI(
    title="Manga Reader API",
    version="0.1.0",
    lifespan=lifespan
)

# --- STATIC FILES ---
# Создаем папку, если её нет (на всякий случай)
if not os.path.exists("media"):
    os.makedirs("media")

# Говорим: "Если запрос начинается на /media, ищи файл в папке media"
app.mount("/media", StaticFiles(directory="media"), name="media")

# Подключаем роуты
# prefix="/api/v1/auth" означает, что адрес будет http://.../api/v1/auth/register
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"]) # <--- Добавили эту строку
app.include_router(manga.router, prefix="/api/v1/manga", tags=["Manga"])
app.include_router(utils.router, prefix="/api/v1/utils", tags=["Utils"])

@app.get("/")
async def root():
    return {"message": "Welcome to Manga Reader API"}


