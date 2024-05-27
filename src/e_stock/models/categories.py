from e_stock.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy_utils import UUIDType
from e_stock.models.associations import product_category_association

from uuid import UUID, uuid4

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, unique=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped[list['Product']] = relationship('Product', secondary=product_category_association, back_populates='categories')