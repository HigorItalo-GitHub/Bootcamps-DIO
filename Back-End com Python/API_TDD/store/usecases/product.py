from decimal import Decimal
from typing import List
from uuid import UUID
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.models.product import ProductModel
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.db.mongo import db_client


class ProductUsecase:
    def __init__(self, collection=None) -> None:
        if collection is not None:
            # nos testes, passamos uma collection fake
            self.collection = collection
        else:
            # em produção, usa Mongo de verdade
            client: AsyncIOMotorClient = db_client.get()
            database: AsyncIOMotorDatabase = client.get_database()
            self.collection = database.get_collection("products")
    
    
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        
        await self.collection.insert_one(product_model.model_dump())
        
        return ProductOut(**product_model.model_dump())


    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        return ProductOut(**result)
    
    
    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]


    async def update(self, id: UUID, body: ProductUpdate) -> ProductOut:
        # Converte o body em dict, ignorando campos não informados
        update_data = body.dict(exclude_unset=True)

        # Converte Decimal para Decimal128 para compatibilidade com MongoDB
        for key, value in update_data.items():
            if isinstance(value, Decimal):
                update_data[key] = Decimal128(value)

        # Atualiza no MongoDB e retorna o documento atualizado
        result = await self.collection.find_one_and_update(
            {"id": id},
            {"$set": update_data},
            return_document=True  # retorna o documento atualizado
        )

        if not result:
            raise Exception("Produto não encontrado")  # ou HTTPException no controller

        # Converte Decimal128 de volta para Decimal ao retornar para o cliente
        if "price" in result and isinstance(result["price"], Decimal128):
            result["price"] = result["price"].to_decimal()

        # Cria objeto ProductOut para retorno
        return ProductUpdateOut(**result)
    
    
    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        result = await self.collection.delete_one({"id": id})
        
        return True if result.deleted_count > 0 else False
    