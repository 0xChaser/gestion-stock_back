from pydantic import BaseModel
from uuid import UUID
from typing import List
from e_stock.schemas.categories import CategoryInDB

class ProductBase(BaseModel):
    name: str
    price: float
    categories: List[CategoryInDB]

class ProductInDB(ProductBase):
    id: UUID

class ProductOut(ProductInDB):
    pass