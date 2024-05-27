from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CategoryBase(BaseModel):
    name: str

class CategoryInDB(CategoryBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class CategoryOut(CategoryInDB):
    pass