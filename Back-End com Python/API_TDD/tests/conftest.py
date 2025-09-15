from decimal import Decimal
import sys, asyncio
from uuid import UUID
import pytest
from tests.usecases.test_product import FakeCollection
from tests.factories import product_data, products_data
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase
from store.main import app
from store.db.mongo import db_client
from httpx import AsyncClient, ASGITransport


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def mongo_client():
    return db_client.get()


@pytest.fixture()
async def clear_collection(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue
        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture()
async def client():
    from store.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_up(product_id):
    return ProductUpdate(
        name="Samsung A1 Neo",
        price="1100.00",
        quantity=10,
        status=True
    )


@pytest.fixture
async def product_inserted(product_in):
    product_usecase = ProductUsecase()
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    product_usecase = ProductUsecase()
    return [await product_usecase.create(body=product_in) for product_in in products_in]


@pytest.fixture
async def product_inserted_fake(product_in):
    fake_collection = FakeCollection()
    usecase = ProductUsecase(collection=fake_collection)
    product = await usecase.create(product_in)

    # sobrescreve o dependency para usar esta mesma fake_collection
    async def override_usecase():
        return ProductUsecase(collection=fake_collection)

    app.dependency_overrides[ProductUsecase] = override_usecase

    yield product, fake_collection

    # limpa para não afetar outros testes
    app.dependency_overrides.clear()

@pytest.fixture
async def products_inserted_fake(products_in):
    fake_collection = FakeCollection()
    usecase = ProductUsecase(collection=fake_collection)
    inserted = [await usecase.create(body=product_in) for product_in in products_in]
    return inserted, fake_collection

