import psycopg2
import os

# Прямые настройки, чтобы исключить ошибки парсинга .env
DB_CONFIG = {
    "dbname": "manga_db",
    "user": "manga_user",
    "password": "manga_password",
    "host": "127.0.0.1",
    "port": "5454"
}

print(f"Testing connection to: {DB_CONFIG['host']}:{DB_CONFIG['port']}...")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("✅ SUCCESS! Обычное (синхронное) подключение работает!")
    print("Значит, база доступна, проблема только в asyncpg.")
    conn.close()
except Exception as e:
    print(f"❌ FAIL! Не удалось подключиться даже обычным способом.")
    print(f"Ошибка: {e}")