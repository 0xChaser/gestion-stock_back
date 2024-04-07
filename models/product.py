from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
