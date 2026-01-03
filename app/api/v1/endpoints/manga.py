import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.schemas.manga import MangaCreate, MangaResponse, MangaDetail, ChapterCreate, ChapterResponse
from app.services import manga_service
from app.models.user import User
from app.schemas.manga import ChapterDetail
from app.services import subscription_service
from app.api.deps import get_current_user_optional

router = APIRouter()

# --- MANGA ENDPOINTS ---

@router.post("/", response_model=MangaResponse, status_code=status.HTTP_201_CREATED)
async def create_manga(
    manga_in: MangaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # Только для авторизованных
):
    """
    Создать новую мангу.
    """
    # Можно добавить проверку, что manga_in.slug уникален, 
    # но пока доверимся ошибке БД, если что.
    return await manga_service.create_manga(db=db, manga_in=manga_in)

@router.get("/", response_model=list[MangaResponse])
async def read_mangas(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список манги (для главной страницы).
    """
    return await manga_service.get_mangas(db=db, skip=skip, limit=limit)

@router.get("/{slug}", response_model=MangaDetail)
async def read_manga_detail(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить полную информацию о манге + список глав.
    Ищем по slug (например, 'naruto'), а не по ID.
    """
    manga = await manga_service.get_manga_by_slug(db=db, slug=slug)
    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")
    return manga

# --- CHAPTER ENDPOINTS ---

@router.post("/{manga_id}/chapters", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def add_chapter(
    manga_id: uuid.UUID,
    chapter_in: ChapterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Добавить главу к манге.
    """
    return await manga_service.create_chapter(db=db, manga_id=manga_id, chapter_in=chapter_in)

@router.get("/chapters/{chapter_id}", response_model=ChapterDetail)
async def read_chapter(
    chapter_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    # Используем Optional, т.к. главу может читать и гость (если она бесплатная)
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    Получить содержимое главы.
    С проверкой прав доступа (Paywall).
    """
    chapter = await manga_service.get_chapter(db=db, chapter_id=chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # 1. Если глава бесплатная — отдаем всем
    if not chapter.is_premium:
        return chapter
    
    # 2. Если глава ПЛАТНАЯ — начинаем проверки
    
    # А. Пользователь должен быть залогинен
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authentication required for premium content"
        )
    
    # Б. У пользователя должна быть активная подписка
    has_sub = await subscription_service.check_subscription(db, user_id=current_user.id)
    if not has_sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Active subscription required to access this chapter"
        )
        
    return chapter