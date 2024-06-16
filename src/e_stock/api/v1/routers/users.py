from fastapi import APIRouter
from e_stock.core.security import fastapi_users
from e_stock.schemas.users import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)
