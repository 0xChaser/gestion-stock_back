from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_stock.exceptions.stocks import StockNotFound
from e_stock.models.stocks import Stock, StockCreate, StockPatch


class StockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        async with self.session as session:
            query = select(Stock)
            result = await session.exec(query)
            return result.all()

    async def add(self, stock: StockCreate):
        async with self.session as session:
            new_stock = Stock.model_validate(stock)
            print(new_stock)
            session.add(new_stock)
            await session.commit()
            await session.refresh(new_stock)
            return new_stock

    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Stock).options(selectinload(Stock.product)).where(Stock.id == id)
            result = await session.exec(query)
            db_stock = result.first()
            if db_stock:
                return db_stock
            raise StockNotFound(id)

    async def patch(self, id: UUID, stock: StockPatch):
        async with self.session as session:
            query = select(Stock).options(selectinload(Stock.product)).where(Stock.id == id)
            result = await session.exec(query)
            db_stock = result.first()
            if db_stock:
                for key, value in stock.model_dump(exclude_unset=True).items():
                    setattr(db_stock, key, value)
                session.add(db_stock)
                await session.commit()
                await session.refresh(db_stock)
                return db_stock
            raise StockNotFound(id)

    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Stock).where(Stock.id == id)
            result = await session.exec(query)
            db_stock = result.first()
            if db_stock:
                await session.delete(db_stock)
                await session.commit()
                return True
            return False
