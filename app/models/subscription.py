import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    
    # Тип подписки (пока просто строка, например "premium")
    plan_type: Mapped[str] = mapped_column(String, default="premium")
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Если дата окончания в будущем — подписка активна
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Связь с юзером
    user: Mapped["User"] = relationship()