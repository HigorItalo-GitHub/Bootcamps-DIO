
from datetime import datetime
from decimal import Decimal
from typing import Optional
from bson import Decimal128
from pydantic import UUID4, BaseModel, Field, model_validator



from store.schemas.base import BaseSchemaMixin, OutMixin


class ProductBase(BaseModel):
    name: str = Field(..., description="product name")
    quantity: int = Field(..., description="product quantity")
    price: Decimal = Field(..., description="product price")
    status: bool = Field(..., description="product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutMixin):
    ...
    # id: UUID4 = Field()
    # created_at: datetime = Field()
    # updated_at: datetime = Field()
    
    # @model_validator(mode="before")
    # def set_schema(cls, data):
    #     for key, value in data.items():
    #         if isinstance(value, Decimal128):
    #             data[key] = Decimal(str(value))
    #     return data
    
    
class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="product quantity")
    price: Optional[Decimal] = Field(None, description="product price")
    status: Optional[bool] = Field(None, description="product status")


class ProductUpdateOut(ProductOut):
    ...