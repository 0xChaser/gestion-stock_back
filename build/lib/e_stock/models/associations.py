from sqlalchemy import Table, Column, ForeignKey
from e_stock.core.database import Base
from sqlalchemy_utils import UUIDType

product_category_association = Table(
    'product_category', Base.metadata,
    Column('product_id', UUIDType, ForeignKey('products.id'), primary_key=True),
    Column('category_id', UUIDType, ForeignKey('categories.id'), primary_key=True),
)