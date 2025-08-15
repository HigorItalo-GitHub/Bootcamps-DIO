from typing import Annotated, Optional
from pydantic import BaseModel, Field, PositiveFloat
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.categorias.schemas import CategoriaIn
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta (BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Higor', max_lenght=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='07205478902', max_lenght=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example='37')]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example='90.5')]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example='1.60')]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_lenght=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Higor', max_lenght=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example='37')]


class AtletaListOut(BaseModel):
    nome: str
    categoria: str
    centro_treinamento: str

    class Config:
        orm_mode = True