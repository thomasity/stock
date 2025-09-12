import httpx
from typing import Iterable, Mapping, Optional
from app.core.config  import settings
from .base import NewsClient

class MarketauxClient(NewsClient):
    BASE = "https://api.marketaux.com/v1/news/all"
    
    async def latest(self, since_iso: Optional[str] = None) -> Iterable[Mapping]:
        if not settings.news_api_key:
            return
        params = {
            "api_token": settings.news_api_key,
            "language": "en",
            "group_similar": "true",
            "must_have_entities": "true",
            "limit": 50
        }
        if since_iso:
            params["published_after"] = since_iso
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(self.BASE, params=params)
            r.raise_for_status()
            for a in r.json().get("data", []):
                yield a
