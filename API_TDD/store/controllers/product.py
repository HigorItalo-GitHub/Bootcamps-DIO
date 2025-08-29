from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase


router = APIRouter(tags=["products"])

def get_product_usecase() -> ProductUsecase:
    # Produção: usa o repositório real (Mongo/Motor)
    return ProductUsecase()

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(body: ProductIn = Body(...), usecase: ProductUsecase = Depends(get_product_usecase)) -> ProductOut:
    return await usecase.create(body=body)

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends(get_product_usecase)) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(id: UUID4 = Path(alias="id"), body: ProductUpdate=Body(...), usecase: ProductUsecase = Depends()) -> ProductOut:
    return await usecase.update(id=id, body=body)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str, 
    usecase: ProductUsecase = Depends()
):
    await usecase.delete(product_id)
    return None