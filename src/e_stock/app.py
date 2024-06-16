from fastapi import FastAPI
from e_stock.api.v1.routers import router as v1_router
from importlib.metadata import version
from fastapi.middleware.cors import CORSMiddleware
from e_stock.core.config import settings
from e_stock.exceptions.base import register_handlers
from e_stock.core.database import init_db


from fastapi import Depends
from e_stock.models.users import User
from e_stock.core.security import current_active_user



app = FastAPI(
    title="e-Stock",
    contact={"name": "Florian ISAK"},
    version=version(__package__),
    root_path="/api",
)

@app.on_event('startup')
async def startup():
    await init_db()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)

register_handlers(app)

@app.get('/protected')
async def protected_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email} !", "user": user}

