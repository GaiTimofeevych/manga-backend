from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.database import engine

# Импортируем наш новый роутер
from app.api.v1.endpoints import auth, users, manga


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    # Тут можно добавить проверку БД, если хочешь, как было раньше
    yield
    print("🛑 Shutting down...")
    await engine.dispose()

app = FastAPI(
    title="Manga Reader API",
    version="0.1.0",
    lifespan=lifespan
)

# Подключаем роуты
# prefix="/api/v1/auth" означает, что адрес будет http://.../api/v1/auth/register
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"]) # <--- Добавили эту строку
app.include_router(manga.router, prefix="/api/v1/manga", tags=["Manga"])

@app.get("/")
async def root():
    return {"message": "Welcome to Manga Reader API"}


