from pydantic import ValidationError
import pytest
# from uuid import UUID

from tests.factories import product_data
from store.schemas.product import ProductIn


def test_schemas_return_success():
    
    data = product_data()
    product = ProductIn.model_validate(data)
    
    assert product.name == "Samsung A1 Neo"
    # assert isinstance(product.id, UUID)

def test_schemas_return_raise():
    data = {'name': "Samsung A1 Neo", 'quantity': 10, 'price': "1000.00"}
    
    with pytest.raises(ValidationError) as erro:
        ProductIn.model_validate(data)
    
    # breakpoint()
    assert erro.value.errors()[0] == {'type': 'missing', 'loc': ('status',), 'msg': 'Field required', 'input': {'name': 'Samsung A1 Neo', 'quantity': 10, 'price': "1000.00"}, 'url': 'https://errors.pydantic.dev/2.11/v/missing'}