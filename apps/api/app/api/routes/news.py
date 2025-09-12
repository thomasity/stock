from fastapi import APIRouter, Query, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from app.db.base import SessionLocal
from app.db.models import Article
from app.schemas.news import ArticleOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ArticleOut])
def latest_news(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    rows = db.execute(select(Article).order_by(Article.published_at.desc()).limit(limit)).scalars().all()
    return [ArticleOut(
        id=a.id, title=a.title, url=a.url, source=a.source,
        published_at=a.published_at, tickers=a.tickers or []
    ) for a in rows]