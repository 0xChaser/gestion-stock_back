from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List
from e_stock.schemas.products import ProductInDB

class StockBase(BaseModel):
    product: ProductInDB
    quantity: int

class StockInDB(StockBase):
    id: UUID

class StockOut(StockInDB):
    model_config = ConfigDict(from_attributes=True)