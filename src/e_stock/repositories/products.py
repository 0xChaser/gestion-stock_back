from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_stock.exceptions.categories import CategoryNotFound
from e_stock.exceptions.products import ProductNotFound
from e_stock.models.categories import Category
from e_stock.models.products import Product, ProductCreate, ProductPatch


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        async with self.session as session:
            query = select(Product)
            result = await session.exec(query)
            response = result.all()
            return response

    async def add(self, product: ProductCreate):
        async with self.session as session:
            # Convertir les catégories publiques en catégories SQLAlchemy
            categories_to_add = []
            for category_public in product.categories:
                existing_category = await session.get(Category, category_public.id)
                if existing_category:
                    categories_to_add.append(existing_category)
                else:
                    raise CategoryNotFound(category_public.id)
            product.categories = categories_to_add

            # Créer le produit en utilisant les catégories converties
            new_product = Product.model_validate(product)

            session.add(new_product)
            await session.commit()
            await session.refresh(new_product)
            return new_product

    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Product).options(selectinload(Product.categories)).where(Product.id == id)
            result = await session.exec(query)
            db_product = result.first()
            if db_product:
                return db_product
            raise ProductNotFound(id)

    async def patch(self, id: UUID, product: ProductPatch):
        async with self.session as session:
            query = select(Product).options(selectinload(Product.categories)).where(Product.id == id)
            result = await session.exec(query)
            db_product = result.first()
            if db_product:
                product_data = product.model_dump(exclude_unset=True)
                for key, value in product_data.items():
                    # Vérifie si la valeur est un dict et convertit en instance SQLAlchemy appropriée
                    if isinstance(value, list) and key == "categories":
                        # Charger les catégories existantes
                        categories = []
                        for category_data in value:
                            category_id = category_data.get("id")
                            if category_id:
                                category = await session.get(Category, category_id)
                                if category:
                                    categories.append(category)
                        value = categories
                    setattr(db_product, key, value)
                session.add(db_product)
                await session.commit()
                await session.refresh(db_product)
                return db_product
            raise ProductNotFound(id)

    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Product).where(Product.id == id)
            result = await session.exec(query)
            product = result.first()
            if product:
                await session.delete(product)
                await session.commit()
                return True
            return False
