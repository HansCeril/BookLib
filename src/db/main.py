from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config

engine = AsyncEngine(
    create_engine(
        config.DATABASE_URL,
        echo=True  # See logs of any SQL queries
    )
)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import BookModel
        await conn.run_sync(SQLModel.metadata.create_all)
