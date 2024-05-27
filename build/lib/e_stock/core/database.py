from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from e_stock.core.config import settings
from sqlalchemy.orm import declarative_base

engine = create_async_engine(
    settings.db_url.__str__(),
    echo=True,
    future=True
)

Base = declarative_base()

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db_session():
    async with async_session() as session:
        yield session