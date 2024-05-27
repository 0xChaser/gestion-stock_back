from e_stock.core.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer
from sqlalchemy_utils import UUIDType
from uuid import UUID, uuid4

class Stock(Base):
    __tablename__ = "stocks"
    
    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, unique=True, nullable=False, default=uuid4)
    quantity: Mapped[int] = mapped_column(Integer())
    product_id: Mapped[UUID] = Column(UUIDType, ForeignKey('products.id'))
    product: Mapped['Product'] = relationship('Product', back_populates="stock")