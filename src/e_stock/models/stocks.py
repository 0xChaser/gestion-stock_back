from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from e_stock.helpers.decorators import optional
from e_stock.models.products import Product, ProductPublic


class StockBase(SQLModel):
    quantity: int


class Stock(StockBase, table=True):
    __tablename__ = "stocks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    product: Product = Relationship(back_populates="stock", sa_relationship_kwargs={"lazy": "selectin"})


class StockPublic(StockBase):
    id: UUID
    product: ProductPublic


class StockCreate(StockBase):
    product_id: UUID


@optional()
class StockPatch(StockBase):
    pass
