from e_stock.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Float
from uuid import UUID, uuid4
from sqlalchemy_utils import UUIDType
from e_stock.models.associations import product_category_association

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, unique=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=True)
    categories: Mapped[list['Category']] = relationship('Category', secondary=product_category_association, back_populates='products')
    stock: Mapped['Stock'] = relationship("Stock", back_populates='product', uselist=False)