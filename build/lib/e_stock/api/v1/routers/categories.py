from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.core.database import get_db_session
from e_stock.repositories.categories import CategoryRepository
from e_stock.schemas.categories import CategoryOut, CategoryBase
from typing import List
from uuid import UUID

router = APIRouter(prefix="/category", tags=["category"])

@router.get('/', response_model=List[CategoryOut])
async def list_categories(session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.list()

@router.post('/', response_model=CategoryOut)
async def create_category(category: CategoryBase, session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.add(category)

@router.patch('/{id}', response_model=CategoryOut)
async def update_category(id: UUID, category: CategoryBase, session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.update(id, category)

@router.delete('/{id}', status_code=204)
async def delete_category(id: UUID, session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.delete(id)