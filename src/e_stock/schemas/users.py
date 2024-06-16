from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from uuid import UUID

class UserRead(BaseUser[UUID]):
    pass

class UserCreate(BaseUserCreate):
    pass

class UserUpdate(BaseUserUpdate):
    pass