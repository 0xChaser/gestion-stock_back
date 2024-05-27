from e_stock.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Boolean
from sqlalchemy_utils import UUIDType
from uuid import UUID, uuid4

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, unique=True, nullable=False, default=uuid4)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)