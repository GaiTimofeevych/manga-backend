import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile

MEDIA_ROOT = Path("media")

async def save_upload_file(file: UploadFile) -> str:
    """
    Сохраняет загруженный файл и возвращает URL.
    """
    # Генерируем уникальное имя: uuid + расширение файла
    # file.filename может быть "cat.jpg". Нам нужно ".jpg"
    extension = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4()}{extension}"
    
    file_path = MEDIA_ROOT / unique_name
    
    # Записываем файл на диск
    # Используем синхронный open для простоты (в тредах FastAPI это ок), 
    # или aiofiles для полной асинхронности. Пока сделаем классически:
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Возвращаем путь, по которому файл будет доступен в браузере
    return f"/media/{unique_name}"