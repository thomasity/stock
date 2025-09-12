from pydantic import BaseModel
from datetime import datetime
from typing import List

class ArticleOut(BaseModel):
    id: str
    title: str
    url: str
    source: str
    published_at: datetime
    tickers: List[str] = []
