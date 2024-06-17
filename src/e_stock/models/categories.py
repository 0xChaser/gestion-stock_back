from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from e_stock.models.associations import ProductCategoriesLink


class CategoryBase(SQLModel):
    name: str = Field(max_length=255, nullable=False)


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True, nullable=False)
    products: list["Product"] = Relationship(
        back_populates="categories", link_model=ProductCategoriesLink, sa_relationship_kwargs={"lazy": "selectin"}
    )


class CategoryPublic(CategoryBase):
    id: UUID
