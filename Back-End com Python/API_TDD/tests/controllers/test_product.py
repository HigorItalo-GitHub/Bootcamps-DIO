from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from uuid import uuid4
import pytest
from httpx import AsyncClient, ASGITransport
from store.main import app
from store.controllers.product import get_product_usecase
from store.usecases.product import ProductUsecase
from tests.factories import product_data
from fastapi import status

# Importa a FakeCollection do local onde foi definida
from tests.usecases.test_product import FakeCollection  # ajusta o caminho se for diferente

pytestmark = pytest.mark.anyio  # garante modo asyncio no arquivo todo

@pytest.fixture(scope="function")
def app_with_fake_usecase():
    fake = FakeCollection()
    usecase = ProductUsecase(collection=fake)

    # override: durante este teste, a rota usará a FakeCollection
    app.dependency_overrides[get_product_usecase] = lambda: usecase
    try:
        yield app, fake
    finally:
        app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def client(app_with_fake_usecase):
    a, _ = app_with_fake_usecase
    transport = ASGITransport(app=a)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    
    del content['id']
    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {"name": "Samsung A1 Neo", "quantity": 10, "price": "1000.00", "status": True,}
 

async def test_controller_get_should_return_sucess(client, products_url):
    # cria produto via POST
    response = await client.post(products_url, json={
        "name": "Samsung A1 Neo",
        "quantity": 10,
        "price": "1000.00",
        "status": True
    })
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()

    # busca produto via GET
    get_response = await client.get(f"{products_url}{content['id']}")
    assert get_response.status_code == status.HTTP_200_OK

    content = get_response.json()

    # removendo campos de data (mudam a cada execução)
    del content['created_at']
    del content['updated_at']

    assert content == {
        "id": content["id"],
        "name": "Samsung A1 Neo",
        "quantity": 10,
        "price": "1000.00",
        "status": True
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"}


@pytest.fixture
def override_dependencies():
    fake_collection = FakeCollection()
    fake_usecase = ProductUsecase(collection=fake_collection)

    # Sobrescreve a dependência ProductUsecase → devolve a versão fake
    app.dependency_overrides[ProductUsecase] = lambda: fake_usecase

    yield fake_collection  # permite popular a coleção no teste

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_controller_query_should_return_success(override_dependencies, products_in):
    fake_collection = override_dependencies

    now = datetime.now(timezone.utc)

    # insere os produtos baseados no fixture products_in
    for product in products_in:
        await fake_collection.insert_one({
            "id": str(uuid4()),
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "status": product.status,
            "created_at": now,
            "updated_at": now,
        })

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/products/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(products_in)
    for expected, received in zip(products_in, data):
        assert expected.name == received["name"]
        assert expected.price == Decimal(received["price"])  # <-- converte string para Decimal
        assert expected.quantity == received["quantity"]
        assert expected.status == received["status"]


@pytest.mark.asyncio
async def test_controller_patch_should_return_success(product_inserted_fake, app_with_fake_usecase):
    product, fake_collection = product_inserted_fake
    app, _ = app_with_fake_usecase  # desempacota o app

    usecase = ProductUsecase(collection=fake_collection)
    app.dependency_overrides[ProductUsecase] = lambda: usecase

    new_price = "1000.00"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch(f"/products/{product.id}", json={"price": new_price})

    content = response.json()
    content.pop("created_at", None)
    content.pop("updated_at", None)

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product.id),
        "name": product.name,
        "quantity": product.quantity,
        "price": new_price,
        "status": product.status,
    }

    app.dependency_overrides.clear()
    

@pytest.mark.anyio
async def test_controller_delete_should_return_no_content(client, product_inserted_fake):
    product, fake_collection = product_inserted_fake

    # sobrescrevendo o usecase para usar a FakeCollection
    async def override_usecase():
        return ProductUsecase(collection=fake_collection)

    app.dependency_overrides[ProductUsecase] = override_usecase

    response = await client.delete(f"/products/{product.id}")

    # limpa override para não afetar outros testes
    app.dependency_overrides.clear()

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # valida se o produto realmente foi removido da FakeCollection
    remaining = await fake_collection.find_one({"id": product.id})
    assert remaining is None
