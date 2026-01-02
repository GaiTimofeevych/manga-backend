import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.manga import Manga, Chapter
from app.schemas.manga import MangaCreate, ChapterCreate

# --- MANGA LOGIC ---
async def create_manga(db: AsyncSession, manga_in: MangaCreate) -> Manga:
    db_manga = Manga(**manga_in.model_dump())
    db.add(db_manga)
    await db.commit()
    await db.refresh(db_manga)
    return db_manga

async def get_mangas(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Manga]:
    stmt = select(Manga).offset(skip).limit(limit).order_by(Manga.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_manga_by_slug(db: AsyncSession, slug: str) -> Manga | None:
    # selectinload подгрузит главы автоматически, т.к. мы указали lazy="selectin" в модели
    stmt = select(Manga).where(Manga.slug == slug)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# --- CHAPTER LOGIC ---
async def create_chapter(db: AsyncSession, manga_id: str, chapter_in: ChapterCreate) -> Chapter:
    db_chapter = Chapter(
        **chapter_in.model_dump(),
        manga_id=manga_id
    )
    db.add(db_chapter)
    await db.commit()
    await db.refresh(db_chapter)
    return db_chapter


async def get_chapter(db: AsyncSession, chapter_id: uuid.UUID) -> Chapter | None:
    stmt = select(Chapter).where(Chapter.id == chapter_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()