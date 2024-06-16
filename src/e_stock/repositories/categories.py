from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.models.categories import Category, CategoryBase
from uuid import UUID

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list(self):
        async with self.session as session:
            query = select(Category)
            result = await session.exec(query)
            return result.scalars().all()
    
    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Category).filter(Category.id == id)
            result = await session.exec(query)
            return result.scalars().first()
    
    async def add(self, category: CategoryBase):
        async with self.session as session:
            new_category = Category.model_validate(category)
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category
    
    async def update(self, id: UUID, category: CategoryBase):
        async with self.session as session:
            db_category = await session.get(Category, id)
            if db_category:
                for key, value in category.model_dump(exclude_unset=True).items():
                    setattr(db_category, key, value)
                session.add(db_category)
                session.commit()
                session.refresh(db_category)
                return db_category
            return None
    
    async def delete(self, id: UUID):
        async with self.session as session:
            category = await session.get(Category, id)
            if category:
                await session.delete(category)
                await session.commit()
                return True
            return False