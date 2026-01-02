import uuid
from datetime import datetime
from sqlalchemy import String, Float, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Manga(Base):
    __tablename__ = "mangas"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True) # Для красивых URL: /manga/naruto
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связь с главами:
    # cascade="all, delete-orphan" удалит все главы, если мы удалим мангу
    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="manga", 
        cascade="all, delete-orphan",
        lazy="selectin" # Важно для асинхронности! Грузит главы сразу одним запросом.
    )

class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    manga_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mangas.id"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    number: Mapped[float] = mapped_column(Float) # Float, чтобы можно было делать главу 10.5
    
    # Список ссылок на страницы: ["url1", "url2"]
    # В PostgreSQL это превратится в JSONB
    pages: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    # Платная ли глава? (Paywall)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связь обратно к манге
    manga: Mapped["Manga"] = relationship(back_populates="chapters")