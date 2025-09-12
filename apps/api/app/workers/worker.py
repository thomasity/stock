import asyncio, logging
from app.core.logging import configure_logging
from app.db.base import init_db
from app.services.news.ingest import run_forever

configure_logging(logging.INFO)
init_db()

async def main():
    await run_forever()

if __name__ == "__main__":
    asyncio.run(main())