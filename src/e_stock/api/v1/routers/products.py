from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from e_stock.core.database import get_db_session
from e_stock.repositories.products import ProductRepository
from e_stock.models.products import ProductPublic, ProductCreate, ProductPatch
from uuid import UUID

router = APIRouter(prefix="/product", tags=["product"])

@router.get('/', response_model=list[ProductPublic])
async def list_products(session: AsyncSession = Depends(get_db_session)):
    prod_repo = ProductRepository(session)
    return await prod_repo.list()

@router.get('/{id}', response_model=ProductPublic)
async def get_product_by_id(id: UUID, session: AsyncSession = Depends(get_db_session)):
    prod_repo = ProductRepository(session)
    return ProductPublic.model_validate(await prod_repo.get_by_id(id))

@router.post('/', response_model=ProductPublic)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_db_session)):
    print(product)
    prod_repo = ProductRepository(session)
    return await prod_repo.add(product)

@router.patch('/{id}', response_model=ProductPublic)
async def patch_product(id: UUID, product: ProductPatch, session: AsyncSession = Depends(get_db_session)):
    prod_repo = ProductRepository(session)
    return await prod_repo.patch(product=product, id=id)

@router.delete('/{id}', status_code=204)
async def delete_product(id: UUID, session: AsyncSession = Depends(get_db_session)):
    prod_repo = ProductRepository(session)
    return await prod_repo.delete(id)