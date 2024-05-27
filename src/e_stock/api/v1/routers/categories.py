from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from e_stock.core.database import get_db_session
from e_stock.repositories.categories import CategoryRepository
from e_stock.schemas.categories import CategoryOut, CategoryBase
from e_stock.exceptions.categories import CategoryNotFound
from typing import List
from uuid import UUID

router = APIRouter(prefix="/category", tags=["category"])

@router.get('/', response_model=List[CategoryOut])
async def list_categories(session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.list()

@router.get('/{id}', response_model=CategoryOut)
async def get_category_by_id(id: UUID, session: AsyncSession = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    result = await cat_repo.get_by_id(id)
    if result:
        return result
    raise CategoryNotFound(id)

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