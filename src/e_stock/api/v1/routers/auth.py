from fastapi import APIRouter

from e_stock.core.security import auth_backend, fastapi_users
from e_stock.schemas.users import UserCreate, UserRead

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"])

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])

# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"]
# )

# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"]
# )
