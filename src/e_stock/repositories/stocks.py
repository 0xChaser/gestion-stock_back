from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from e_stock.models.stocks import Stock
from e_stock.models.products import Product
from e_stock.schemas.stocks import StockBase, StockOut
from e_stock.schemas.products import ProductInDB
from e_stock.schemas.categories import CategoryInDB
from e_stock.exceptions.products import ProductNotFound
from uuid import UUID
from e_stock.repositories.products import ProductRepository
from e_stock.repositories.categories import CategoryRepository


class StockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list(self):
        async with self.session as session:
            query = select(Stock).options(
                joinedload(Stock.product).joinedload(Product.categories)
            )
            result = await session.execute(query)
            stocks = result.unique().scalars().all()

            stock_out_list = []
            for stock in stocks:
                if stock.product:  # Ensure the product is not None
                    # Ensure product categories are fully loaded
                    categories = [CategoryInDB.model_validate(cat) for cat in stock.product.categories]
                    product_dict = ProductInDB.model_validate(stock.product).model_dump()
                    product_dict['categories'] = categories
                    stock_out_dict = StockOut.model_validate(stock).model_dump()
                    stock_out_dict['product'] = product_dict
                    stock_out_list.append(StockOut(**stock_out_dict))
                else:
                    # Handle the case where product is None, if necessary
                    continue

            return stock_out_list
    
    async def get_by_id(self, id: UUID):
        async with self.session as session:
            query = select(Stock).options(
                joinedload(Stock.product).joinedload(Product.categories)
            ).filter(Stock.id == id)
            result = await session.execute(query)
            stock = result.scalars().first()
            if stock and stock.product:
                # Ensure product categories are fully loaded
                categories = [CategoryInDB.model_validate(cat) for cat in stock.product.categories]
                product_dict = ProductInDB.model_validate(stock.product).model_dump()
                product_dict['categories'] = categories
                stock_out_dict = StockOut.model_validate(stock).model_dump()
                stock_out_dict['product'] = product_dict
                return StockOut(**stock_out_dict)
            elif stock:
                return StockOut.model_validate(stock)
            return None
    
    async def add(self, stock: StockBase):
        async with self.session as session:
            prod_repo = ProductRepository(session)
            cat_repo = CategoryRepository(session)
            product = await prod_repo.get_by_id(stock.product.id)
            if not product:
                raise ProductNotFound(stock.product.id)

            # Use the already loaded categories from the product instance
            stock_dict = stock.model_dump()
            stock_dict['product'] = product
            new_stock = Stock(**stock_dict)

            # Ensure the product instance is merged into the session to avoid duplicates
            session.merge(product)

            session.add(new_stock)
            await session.commit()
            await session.refresh(new_stock)
            
            # Convert to StockOut schema before returning to avoid DetachedInstanceError
            return StockOut.model_validate(new_stock)
    
    async def update(self, id: UUID, stock: StockBase):
        async with self.session as session:
            query = select(Stock).filter(Stock.id == id)
            result = await session.execute(query)
            db_stock = result.scalars().first()
            if db_stock:
                for key, value in stock.model_dump().items():
                    setattr(db_stock, key, value)
                await session.commit()
                return db_stock
            return None
    
    async def delete(self, id: UUID):
        async with self.session as session:
            query = select(Stock).filter(Stock.id == id)
            result = await session.execute(query)
            stock = result.scalars().first()
            if stock:
                await session.delete(stock)
                await session.commit()
                return True
            return False