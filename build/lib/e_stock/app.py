from fastapi import FastAPI
from e_stock.api.v1.routers import router as v1_router
from importlib.metadata import version

app = FastAPI(
    title="e-Stock",
    contact={"name": "Florian ISAK"},
    version=version(__package__),
    openapi_prefix="/api"
)

app.include_router(v1_router)

