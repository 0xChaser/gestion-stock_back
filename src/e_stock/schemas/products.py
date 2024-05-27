from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List
from e_stock.schemas.categories import CategoryInDB

class ProductBase(BaseModel):
    name: str
    price: float
    categories: List[CategoryInDB]

class ProductPatch(BaseModel):
    name: str | None
    price: float | None
    categories: List[CategoryInDB] | None

class ProductInDB(ProductBase):
    id: UUID
    model_config= ConfigDict(from_attributes=True)

class ProductOut(ProductInDB):
    pass