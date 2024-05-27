from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.models.products import Product
from e_stock.models.categories import Category
from e_stock.schemas.products import ProductBase, ProductPatch
from e_stock.exceptions.categories import CategoryNotFound
from uuid import UUID

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list(self):
        async with self.session as session:
            query = select(Product).options(joinedload(Product.categories))
            result = await session.execute(query)
            return result.unique().scalars().all()
    
    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Product).options(joinedload(Product.categories)).filter(Product.id == id)
            result = await session.execute(query)
            return result.scalars().first()
    
    async def add(self, product: ProductBase):
        async with self.session as session:
            categories = []
            for category_dict in product.categories:
                category = await session.get(Category, category_dict.id)
                if category:
                    categories.append(category)
                else:
                    raise CategoryNotFound(category_dict.id)
            product_dict = product.model_dump()
            product_dict['categories'] = categories
            new_product = Product(**product_dict)
            session.add(new_product)
            await session.commit()
            return new_product
    
    async def update(self, id: UUID, product: ProductBase):
        async with self.session as session:
            query = select(Product).filter(Product.id == id)
            result = await session.execute(query)
            db_product = result.scalars().first()
            if db_product:
                product_dict = product_dict.model_dump()
                if 'categories' in product_dict:
                    categories = []
                    for category_dict in product_dict['categories']:
                        category = await session.get(Category, category_dict.id)
                        if category:
                            categories.append(category)
                        else:
                            raise CategoryNotFound(category_dict.id)
                for key, value in product_dict.items():
                    setattr(db_product, key, value)
                await session.commit()
                return db_product
            return None
    
    async def patch(self, id: UUID, product: ProductPatch):
        async with self.session as session:
            query = select(Product).filter(Product.id == id)
            result = await session.execute(query)
            db_product = result.scalars().first()
            if db_product:
                product_dict = product.model_dump()
                if 'categories' in product_dict and product_dict['categories'] is not None:
                    categories = []
                    for category_dict in product_dict['categories']:
                        category = await session.get(Category, category_dict.id)
                        if category:
                            categories.append(category)
                        else:
                            raise CategoryNotFound(category_dict.id)
                for key, value in product.model_dump().items():
                    if value is not None:
                        setattr(db_product, key, value)
                await session.commit()
                return db_product
            return None

    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Product).filter(Product.id == id)
            result = await session.execute(query)
            product = result.scalars().first()
            if product:
                await session.delete(product)
                await session.commit()
                return True
            return False