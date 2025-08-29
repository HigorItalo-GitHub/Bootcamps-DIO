from typing import List
import pytest
from uuid import UUID, uuid4
from store.core.exceptions import NotFoundException
from store.usecases.product import ProductUsecase
from store.schemas.product import ProductIn, ProductOut, ProductUpdateOut


class FakeDeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count
        
        
class FakeCollection:
    def __init__(self):
        self.storage = {}

    async def insert_one(self, doc):
        self.storage[str(doc["id"])] = doc
        return doc

    async def find_one(self, query):
        return self.storage.get(str(query["id"]))
    
    def find(self):
        # Mongo retorna um "cursor" iterável (não async generator direto)
        # Aqui simulamos como um async generator
        async def generator():
            for item in self.storage.values():
                yield item
        return generator()
    
    async def find_one_and_update(self, filter, update, return_document=None):
        key = str(filter["id"])
        item = self.storage.get(key)
        if not item:
            return None

        if "$set" in update:
            item.update(update["$set"])
        elif "set" in update:
            item.update(update["set"])

        self.storage[key] = item
        return item

    async def delete_one(self, filter):
        key = str(filter["id"])
        if key in self.storage:
            del self.storage[key]
            return FakeDeleteResult(deleted_count=1)
        return FakeDeleteResult(deleted_count=0)


@pytest.mark.asyncio
async def test_usecases_create_should_return_sucess():
    fake_collection = FakeCollection()
    usecase = ProductUsecase(collection=fake_collection)

    body = ProductIn(
        name="Samsung A1 Neo",
        price="1000.00",
        quantity=10,
        status=True
    )

    created = await usecase.create(body)

    assert isinstance(created, ProductOut)
    assert created.name == body.name
    assert created.price == body.price
    assert created.quantity == body.quantity
    assert created.status == body.status


async def test_usecases_get_should_return_sucess(product_inserted_fake):
    product, fake_collection = product_inserted_fake
    usecase = ProductUsecase(collection=fake_collection)

    result = await usecase.get(product.id)

    assert result is not None
    assert result.id == product.id    


@pytest.mark.asyncio
async def test_usecases_get_should_not_found():
    fake_collection = FakeCollection()
    usecase = ProductUsecase(collection=fake_collection)
    
    with pytest.raises(NotFoundException) as erro:
        await usecase.get(id=UUID('1e4f21ae-85f7-461a-89d0-a751a32e3bb9'))
        
    assert erro.value.message == "Product not found with filter: 1e4f21ae-85f7-461a-89d0-a751a32e3bb9"


@pytest.mark.asyncio
async def test_usecases_query_should_return_sucess(products_inserted_fake):
    inserted, fake_collection = products_inserted_fake
    usecase = ProductUsecase(collection=fake_collection)

    result = await usecase.query()

    assert isinstance(result, list)
    assert len(result) > 1


@pytest.mark.asyncio
async def test_usecases_update_should_return_sucess(product_inserted_fake, product_up):
    product, fake_collection = product_inserted_fake
    usecase = ProductUsecase(collection=fake_collection)

    result = await usecase.update(id=product.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
    assert result.price == 1100.00


@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(product_inserted_fake):
    product, fake_collection = product_inserted_fake
    usecase = ProductUsecase(collection=fake_collection)
    
    result = await usecase.delete(id=product.id)

    assert result is True


@pytest.mark.asyncio
async def test_usecases_delete_should_not_found():
    fake_collection = FakeCollection()
    usecase = ProductUsecase(collection=fake_collection)
    
    with pytest.raises(NotFoundException) as erro:
        await usecase.delete(id=UUID('1e4f21ae-85f7-461a-89d0-a751a32e3bb9'))
        
    assert erro.value.message == "Product not found with filter: 1e4f21ae-85f7-461a-89d0-a751a32e3bb9"