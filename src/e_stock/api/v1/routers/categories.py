from fastapi import APIRouter, Depends
from sqlmodel import Session
from e_stock.core.database import get_db_session
from e_stock.models.categories import CategoryBase, Category
from e_stock.repositories.categories import CategoryRepository
from e_stock.exceptions.categories import CategoryNotFound
from uuid import UUID

router = APIRouter(prefix="/category", tags=["category"])

@router.get('/')
async def list_categories(session: Session = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.list()

@router.get('/{id}')
async def get_category_by_id(id: UUID, session: Session = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    result = await cat_repo.get_by_id(id)
    if result:
        return result
    raise CategoryNotFound(id)

@router.post('/', response_model=Category)
async def create_category(category: CategoryBase, session: Session = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.add(category)

@router.patch('/{id}')
async def update_category(id: UUID, category: CategoryBase, session: Session = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.patch(id, category)

@router.delete('/{id}', status_code=204)
async def delete_category(id: UUID, session: Session = Depends(get_db_session)):
    cat_repo = CategoryRepository(session)
    return await cat_repo.delete(id)