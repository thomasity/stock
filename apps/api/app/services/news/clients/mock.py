from typing import Iterable, Mapping, Optional
from datetime import datetime, timezone
import uuid, random

SOURCES = ["Reuters","WSJ","Bloomberg","CNBC"]
TITLES = [
    "AAPL guides up on strong iPhone demand",
    "NVDA announces new GPU line for data centers",
    "MSFT to acquire small AI startup",
    "AMZN expands same-day delivery coverage",
]


class MockClient:
    async def latest(self, since_iso: Optional[str] = None) -> Iterable[Mapping]:
        now = datetime.now(timezone.utc).isoformat()
        for _ in range(random.randint(1, 5)):
            t = random.choice(TITLES)
            yield {
                "uuid": str(uuid.uuid4()),
                "title": t,
                "url": "https://example.com/article/" + str(uuid.uuid4())[:8],
                "source": random.choice(SOURCES),
                "published_at": now,
                "entities": [{"type":"equity","symbol": s} for s in ["AAPL","NVDA","MSFT","AMZN"] if s in t],
            }