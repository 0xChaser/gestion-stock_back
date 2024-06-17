from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from e_stock.core.database import get_db_session
from e_stock.models.stocks import StockCreate, StockPatch, StockPublic
from e_stock.repositories.stocks import StockRepository

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/", response_model=list[StockPublic])
async def list_stocks(session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.list()


@router.get("/{id}", response_model=StockPublic)
async def get_by_id(id: UUID, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.get_by_id(id)


@router.post("/", response_model=StockPublic)
async def create_stock(stock: StockCreate, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.add(stock)


@router.patch("/{id}", response_model=StockPublic)
async def patch_stock(id: UUID, stock: StockPatch, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.patch(id, stock)


@router.delete("/{id}", status_code=204)
async def delete_stock(id: UUID, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.delete(id)
