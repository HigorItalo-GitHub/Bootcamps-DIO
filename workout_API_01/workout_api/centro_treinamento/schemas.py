from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT Laranjeiras', max_lenght=20)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', example='Rua COB, 001, Centro, Brasilia-DF', max_lenght=60)]
    proprietario: Annotated[str, Field(description='proprietário do Centro de Treinamento', example='CP Ciqueira', max_lenght=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT Laranjeiras', max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamaneto')]    