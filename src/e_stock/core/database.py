from fastapi import Depends
from e_stock.core.config import settings
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from e_stock.models.users import User


engine = AsyncEngine(create_engine(settings.db_url.__str__(), echo=True, future=True))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db_session():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_db_session)):
    yield SQLModelUserDatabaseAsync(session, User)
