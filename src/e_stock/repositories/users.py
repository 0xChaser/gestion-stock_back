from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlmodel import select

from e_stock.core.config import settings
from e_stock.core.database import get_user_db
from e_stock.models.users import User


class UserRepository(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.secret_key.get_secret_value()
    verification_token_secret = settings.secret_key.get_secret_value()

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        print(f"User {user.id} has registered.")
        return await super().on_after_register(user, request)

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        return await super().on_after_forgot_password(user, token, request)

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        return await super().on_after_request_verify(user, token, request)

    async def get_all_users(self):
        query = select(User)
        result = await self.user_db.session.exec(query)
        return result.all()


async def get_user_manager(user_db: SQLModelUserDatabase = Depends(get_user_db)):
    yield UserRepository(user_db)
