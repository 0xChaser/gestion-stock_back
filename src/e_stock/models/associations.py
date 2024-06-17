from uuid import UUID

from sqlmodel import Field, SQLModel


class ProductCategoriesLink(SQLModel, table=True):
    product_id: UUID = Field(default=None, foreign_key="products.id", primary_key=True)
    category_id: UUID = Field(default=None, foreign_key="categories.id", primary_key=True)
