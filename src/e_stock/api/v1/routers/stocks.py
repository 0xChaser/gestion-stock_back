from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.core.database import get_db_session
from e_stock.repositories.stocks import StockRepository
from e_stock.schemas.stocks import StockOut, StockBase
from typing import List
from uuid import UUID

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get('/', response_model=List[StockOut])
async def list_stocks(session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.list()

@router.get('/{id}', response_model=StockOut)
async def get_stock_by_id(id: UUID, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.get_by_id(id)

@router.post('/', response_model=StockOut)
async def create_stock(stock: StockBase, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.add(stock)

@router.patch('/{id}', response_model=StockOut)
async def update_stock(id: UUID, stock: StockBase, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.update(id, stock)

@router.delete('/{id}', status_code=204)
async def delete_stock(id: UUID, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.delete(id)