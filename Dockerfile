# 1. Используем официальный легкий образ Python
FROM python:3.12-slim

# 2. Переменные окружения для Python
# PYTHONDONTWRITEBYTECODE - не создавать .pyc файлы
# PYTHONUNBUFFERED - выводить логи сразу в консоль
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Poetry настройки: не создавать virtualenv внутри докера (не нужно)
    POETRY_VIRTUALENVS_CREATE=false

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Устанавливаем системные зависимости (нужны для сборки некоторых питон-пакетов)
# curl нужен для установки poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# 6. Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# 7. Устанавливаем зависимости (без dev-пакетов, чтобы образ был меньше)
RUN poetry install --no-root --no-interaction --no-ansi

# 8. Копируем весь остальной код проекта
COPY . .

# 9. Команда запуска (используем shell-скрипт, чтобы сначала прогнать миграции)
# Создадим скрипт запуска прямо тут или отдельным файлом.
# Для простоты пропишем команду запуска uvicorn напрямую.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]