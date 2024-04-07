from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, nullable=False)
