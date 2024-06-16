from e_stock.api.v1.routers.auth import router as auth_router
from e_stock.api.v1.routers.categories import router as category_router
from e_stock.api.v1.routers.products import router as product_router
from e_stock.api.v1.routers.stocks import router as stock_router
from e_stock.api.v1.routers.users import router as user_router
from fastapi import APIRouter

__all__ = [
    auth_router,
    category_router,
    product_router,
    stock_router,
    user_router
]

router = APIRouter(prefix="/v1")
for api_router in __all__:
    router.include_router(api_router)
