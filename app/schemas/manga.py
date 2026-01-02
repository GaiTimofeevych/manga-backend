import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- CHAPTER SCHEMAS ---
class ChapterBase(BaseModel):
    title: str
    number: float
    is_premium: bool = False

class ChapterCreate(ChapterBase):
    pages: list[str] # При создании мы ожидаем список URL картинок

class ChapterResponse(ChapterBase):
    id: uuid.UUID
    manga_id: uuid.UUID
    created_at: datetime
    # Pages мы здесь НЕ возвращаем по умолчанию, чтобы не грузить лишнее в списках
    
    model_config = ConfigDict(from_attributes=True)

class ChapterDetail(ChapterResponse):
    pages: list[str] # А вот когда читаем главу — страницы нужны

# --- MANGA SCHEMAS ---
class MangaBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    cover_image: str | None = None

class MangaCreate(MangaBase):
    pass

class MangaResponse(MangaBase):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class MangaDetail(MangaResponse):
    # При просмотре одной манги мы хотим видеть список её глав
    chapters: list[ChapterResponse] = []