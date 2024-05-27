from fastapi import FastAPI
from e_stock.api.v1.routers import router as v1_router
from importlib.metadata import version
from fastapi.middleware.cors import CORSMiddleware
from e_stock.core.config import settings
from e_stock.exceptions.base import register_handlers

app = FastAPI(
    title="e-Stock",
    contact={"name": "Florian ISAK"},
    version=version(__package__),
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)

register_handlers(app)