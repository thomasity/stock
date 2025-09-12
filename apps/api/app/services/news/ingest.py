import asyncio, logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.config import settings
from app.db.base import SessionLocal
from app.db.models import Article
from app.services.news.dedup import Deduper
from app.services.news.clients.marketaux import MarketauxClient
from app.services.news.clients.mock import MockClient

log = logging.getLogger(__name__)

def _client():
    return MarketauxClient() if settings.news_api_key else MockClient()

def _normalize(raw: dict) -> dict:
    return {
        "id": raw.get("uuid") or raw.get("id"),
        "title": raw.get("title"),
        "url": raw.get("url"),
        "source": (raw.get("source") or raw.get("source_name") or "unknown"),
        "published_at": raw.get("published_at"),
        "entities": raw.get("entities") or [],
        "tickers": [e.get("symbol") for e in raw.get("entities", []) if (e.get("type") or "").lower()=="equity"],
    }

async def run_forever():
    client = _client()
    dedup = Deduper()
    cursor: str | None = None
    
    while True:
        try:
            async for raw in client.latest(cursor):
                if dedup.is_dup(raw):
                    continue
                norm = _normalize(raw)
                
                try:
                    published = datetime.fromisoformat(norm["published_at"]).strftime("%Y-%m-%dT%H:%M")
                except Exception:
                    published = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
                
                with SessionLocal() as db:
                    a = Article(
                        id=norm["id"], title=norm["title"], url=norm["url"], source=norm["source"],
                        published_at=published, entities=norm["entities"], tickers=norm["tickers"],
                        hash=dedup.key(raw),
                    )
                    exists = db.execute(select(Article.id).where(Article.hash == a.hash)).first()
                    if exists:
                        continue
                    db.add(a); db.commit()
                
                log.info("ingested: %s | %s", norm["source"], norm["title"][:80])
            
            cursor = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        except Exception as e:
            log.exception("ingest error: %s", e)
        log.debug("waiting %s seconds until next poll...", settings.news_poll_seconds)
        await asyncio.sleep(settings.news_poll_seconds)