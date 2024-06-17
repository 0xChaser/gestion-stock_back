from uuid import UUID

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)

from e_stock.core.config import settings
from e_stock.models.users import User
from e_stock.repositories.users import get_user_manager

bearer_transport = BearerTransport(tokenUrl="api/v1/auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret_key.get_secret_value(), lifetime_seconds=settings.token_lifetime_in_seconds
    )


auth_backend = AuthenticationBackend(name="default", transport=bearer_transport, get_strategy=get_jwt_strategy)

fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
