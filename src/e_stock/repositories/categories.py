from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from e_stock.models.categories import Category, CategoryBase


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        async with self.session as session:
            query = select(Category)
            result = await session.exec(query)
            return result.all()

    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Category).filter(Category.id == id)
            result = await session.exec(query)
            return result.first()

    async def add(self, category: CategoryBase):
        async with self.session as session:
            new_category = Category.model_validate(category)
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category

    async def patch(self, id: UUID, category: CategoryBase):
        async with self.session as session:
            query = select(Category).where(Category.id == id)
            result = await session.exec(query)
            db_category = result.first()
            if db_category:
                for key, value in category.model_dump(exclude_unset=True).items():
                    setattr(db_category, key, value)
                session.add(db_category)
                await session.commit()
                await session.refresh(db_category)
                return db_category
            return None

    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Category).where(Category.id == id)
            result = await session.exec(query)
            category = result.first()
            if category:
                await session.delete(category)
                await session.commit()
                return True
            return False
