from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.categorias.models import CategoriaModel
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaListOut, AtletaOut, AtletaUpdate

from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn=Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'A categoria {categoria_nome} não foi encontrada.')
    
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.')
    
    # try:
    #     atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(timezone.utc), **atleta_in.model_dump())
    #     atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        
    #     atleta_model.categoria_id = categoria.pk_id
    #     atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
    #     db_session.add(atleta_model)
    #     await db_session.commit()
    # except Exception as e:
    #     raise HTTPException(
    #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     detail=f'Ocorreu um erro ao inserir os dados no banco: {str(e)}'
    #     )
    
    try:
        atleta_model = AtletaModel(
            id=uuid4(),
            nome=atleta_in.nome,
            cpf=atleta_in.cpf,
            idade=atleta_in.idade,
            peso=atleta_in.peso,
            altura=atleta_in.altura,
            sexo=atleta_in.sexo,
            categoria_id=categoria.pk_id,
            centro_treinamento_id=centro_treinamento.pk_id,
            created_at=datetime.now(timezone.utc),
        )

        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)

        return AtletaOut.model_validate(atleta_model)

    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
    
    # return atleta_out

@router.get(
    '/', 
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaListOut],
)
async def query(db_session: DatabaseDependency, nome: Optional[str] = None, cpf: Optional[str] = None,) -> list[AtletaListOut]:
    
    # atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    stmt = select(AtletaModel).options(selectinload(AtletaModel.categoria),selectinload(AtletaModel.centro_treinamento))
    
    # adiciona filtros caso os parâmetros sejam enviados
    if nome:
        stmt = stmt.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        stmt = stmt.filter(AtletaModel.cpf == cpf)

    result = await db_session.execute(stmt)
    atletas = result.scalars().all()
    
    return [AtletaListOut(
            nome=atleta.nome,
            categoria=atleta.categoria.nome,
            centro_treinamento=atleta.centro_treinamento.nome
        ) for atleta in atletas]

@router.get(
    '/',
    summary='Consultar atletas com paginação',
    response_model=Page[AtletaListOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
) -> Page[AtletaListOut]:
    
    stmt = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento)
    )

    if nome:
        stmt = stmt.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        stmt = stmt.filter(AtletaModel.cpf == cpf)

    # aqui é o segredo: em vez de executar e retornar manualmente,
    # usamos paginate(...)
    return await paginate(db_session, stmt)

@router.get(
    '/{id}', 
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency, atleta_update: AtletaUpdate=Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    atleta_up_dt = atleta_update.model_dump(exclude_unset=True)
    for key, value in atleta_up_dt.items():
        setattr(atleta, key, value)
        
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def get(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()
