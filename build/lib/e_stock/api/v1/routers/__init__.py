from e_stock.api.v1.routers.categories import router as category_router
from fastapi import APIRouter

__all__ = [
    category_router
]

router = APIRouter(prefix="/v1")
for api_router in __all__:
    router.include_router(api_router)
