import logging
from fastapi import FastAPI
from app.core.logging import configure_logging
from app.core.config import settings
from app.db.base import init_db
from app.api.routes import health, news, control, broker, portfolio

configure_logging()
logging.getLogger("startup").info(
    "config: news_poll_seconds=%s (env=%s)",
    settings.news_poll_seconds,
    settings.app_env,
)
logging.getLogger("startup").info("DATABASE_URL=%r", settings.database_url)
# init_db()

app = FastAPI(title="Stock Trade Engine API", version="0.1.0")
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(control.router, prefix="/api/control", tags=["control"])
app.include_router(broker.router, prefix="/api/broker", tags=["broker"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])

@app.get("/")
def index():
    return {"message": "engine ok", "env": settings.app_env}