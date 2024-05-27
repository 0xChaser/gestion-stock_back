from pydantic import BaseModel
from uuid import UUID


class CategoryBase(BaseModel):
    name: str

class CategoryInDB(CategoryBase):
    id: UUID

class CategoryOut(CategoryInDB):
    pass