from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    id: UUID
    username: str
    is_admin: bool = False

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    pass