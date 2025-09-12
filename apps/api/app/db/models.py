from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, Index
from datetime import datetime, timezone
from app.db.base import Base

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(1024))
    source: Mapped[str] = mapped_column(String(128))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    entities: Mapped[dict] = mapped_column(JSON, default=dict)
    tickers: Mapped[list] = mapped_column(JSON, default=list)
    hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

Index("ix_articles_published", Article.published_at)
Index("ix_articles_hash", Article.hash, unique=True)