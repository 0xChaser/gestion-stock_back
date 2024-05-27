from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.models.categories import Category
from e_stock.schemas.categories import CategoryBase
from uuid import UUID

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list(self):
        async with self.session as session:
            query = select(Category)
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Category).filter(Category.id == id)
            result = await session.execute(query)
            return result.scalars().first()
    
    async def add(self, category: CategoryBase):
        async with self.session as session:
            new_category = Category(**category.model_dump())
            session.add(new_category)
            await session.commit()
            return new_category
    
    async def update(self, id: UUID, category: CategoryBase):
        async with self.session as session:
            query = select(Category).filter(Category.id == id)
            result = await session.execute(query)
            db_category = result.scalars().first()
            if db_category:
                for key, value in category.model_dump().items():
                    setattr(db_category, key, value)
                await session.commit()
                return db_category
            return None
    
    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Category).filter(Category.id == id)
            result = await session.execute(query)
            category = result.scalars().first()
            if category:
                await session.delete(category)
                await session.commit()
                return True
            return False