from fastapi import APIRouter, Depends
from e_stock.models.stocks import StockPublic, StockCreate, StockPatch
from e_stock.core.database import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from e_stock.repositories.stocks import StockRepository
from uuid import UUID


router = APIRouter(prefix="/stock", tags=['stock'])

@router.get('/', response_model=list[StockPublic])
async def list_stocks(session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.list()

@router.post('/', response_model=StockPublic)
async def create_stock(stock: StockCreate, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.add(stock)

@router.patch('/{id}', response_model=StockPublic)
async def patch_stock(id: UUID, stock: StockPatch, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.patch(id, stock)

@router.delete('/{id}', status_code=204)
async def delete_stock(id: UUID, session: AsyncSession = Depends(get_db_session)):
    stock_repo = StockRepository(session)
    return await stock_repo.delete(id)