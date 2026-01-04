import pytest
import uuid
from httpx import AsyncClient

# Генерируем случайный email для каждого запуска
def random_email():
    return f"tester_{uuid.uuid4()}@example.com"

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    email = random_email()
    payload = {
        "username": f"user_{uuid.uuid4()}",
        "email": email,
        "password": "securepassword123"
    }
    
    response = await client.post("/api/v1/auth/register", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "id" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    email = random_email()
    payload = {
        "username": f"user_{uuid.uuid4()}",
        "email": email,
        "password": "password"
    }
    
    # 1. Создаем первого
    await client.post("/api/v1/auth/register", json=payload)
    
    # 2. Пытаемся создать второго с тем же email
    # (username меняем, чтобы проверить именно уникальность email)
    payload["username"] = "other_user"
    response = await client.post("/api/v1/auth/register", json=payload)
    
    assert response.status_code == 400