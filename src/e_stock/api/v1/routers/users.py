from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from e_stock.core.database import get_user_db
from e_stock.core.security import current_superuser, fastapi_users
from e_stock.models.users import User
from e_stock.repositories.users import UserRepository
from e_stock.schemas.users import UserRead, UserUpdate

router = APIRouter(prefix="/user", tags=["users"])

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/user", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(get_user_db), user: User = Depends(current_superuser)):
    user_repo = UserRepository(session)
    return await user_repo.get_all_users()
