from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from e_stock.helpers.decorators import optional
from e_stock.models.associations import ProductCategoriesLink
from e_stock.models.categories import Category, CategoryPublic


class ProductBase(SQLModel):
    name: str = Field(index=True)
    price: float


class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    categories: list["Category"] = Relationship(
        back_populates="products", link_model=ProductCategoriesLink, sa_relationship_kwargs={"lazy": "selectin"}
    )
    stock: Optional["Stock"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "selectin"})


class ProductPublic(ProductBase):
    id: UUID
    categories: list[Category] = []


class ProductCreate(ProductBase):
    categories: list[CategoryPublic] = []


@optional()
class ProductPatch(ProductCreate):
    pass
