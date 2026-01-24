import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Manga(Base): # Создаем класс Манга и наследуем его от Базового
  __tablename__ = "mangas" # Создаем таблицу чтобы SQLAlchemy не создал сам таблицу с рандомным названием

  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4) # Создаем колонку id чтобы был индивидуальный идентификатор также с помощью Mapped указываем явно вскоду что здесь будем uuid тип данных, а также делаем primary_key чтобы таблица по этому связывалась с другими таблицами и чтобы id был uuid чтобы его нельзя было отследить
  title: Mapped[str] = mapped_column(String(255), index=True) # Создаем колонку title чтобы было название манги, также указываем размер в 255 символов и делаем индекс чтобы было удобно искать по названию
  slug: Mapped[str] = mapped_column(String(255), unique=True, index=True) # Создаем колонку slug чтобы было красивое название манги, также делаем его уникальным и индексируем
  description: Mapped[str|None] = mapped_column(Text, nullable=True) # Создаем колонку description чтобы было описание манги, также делаем nullable чтобы описание было необязательным
  cover_image: Mapped[str|None] = mapped_column(String, nullable=True) # Создаем колонку cover_image чтобы было обложка манги, также делаем nullable чтобы обложка была необязательной
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) # Создаем колонку created_at чтобы было время создания манги, также делаем server_default чтобы время создания было текущим также делаем timezone=True чтобы время было в часовом поясе и вызываем функцию func.now() чтобы время было текущим ее импортируем из sqlalchemy.sql

  chapters: Mapped[list["Chapter"]] = relationship(  # Создаем отношения двух таблиц вид отношений один ко многим (так как у одной манги может быть много глав, но у главы только одна манга)
    back_populates = 'manga', # Связь в обратную сторону
    cascade = 'all, delete-orphan', # Если манга удалится, то и главы тоже удалятся delete-orphan чтобы не было пустых глав
    lazy = 'selectin' # Загружаем главы сразу, а не по одному
  )

class Chapter(Base): # Создаем класс Глава и наследуем его от Базового
  __tablename__ = 'chapters' # Создаем таблицу чтобы SQLAlchemy не создал саму таблицу с рандомным названием

  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4) # Создаем колонку id чтобы был индивидуальный идентификатор также с помощью Mapped указываем явно вскоду что здесь будем uuid тип данных, а также делаем primary_key чтобы таблица по этому связывалась с другими таблицами и чтобы id был uuid чтобы его нельзя было отследить
  manga_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('mangas.id'), index=True) # Создаем колонку manga_id чтобы было id манги, также делаем ForeignKey чтобы id манги был из таблицы mangas и делаем index чтобы было удобно искать по id манги
  title: Mapped[str] = mapped_column(String(255)) # Создаем колонку title чтобы было название главы, также указываем размер в 255 символов
  number: Mapped[float] = mapped_column(Float) # Создаем колонку number чтобы было номер главы, также делаем Float чтобы число было с плавающей точкой
  pages: Mapped[list[str]] = mapped_column(JSON, default=list) # Создаем колонку pages чтобы было список страниц, также делаем JSON чтобы список был в формате JSON и указываем default=list чтобы список был пустым
  is_premium: Mapped[bool] = mapped_column(Boolean, default=False) # Создаем колонку is_premium чтобы было премиум глава или нет, также делаем Boolean чтобы значение было булевым и указываем default=False чтобы значение было False
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) # Создаем колонку created_at чтобы было время создания главы, также делаем server_default чтобы время создания было текущим также делаем timezone=True чтобы время было в часовом поясе и вызываем функцию func.now() чтобы время было текущим ее импортируем из sqlalchemy.sql

  manga: Mapped["Manga"] = relationship(back_populates="chapters") # Создаем отношения двух таблиц вид отношений многие к одному (так как у одной главы может быть только одна манга, но у манги может быть много глав)