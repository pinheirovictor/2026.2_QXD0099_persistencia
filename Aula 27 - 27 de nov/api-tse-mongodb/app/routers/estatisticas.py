"""Agregações descritivas, em ordem alfabética para não produzir rankings."""
from fastapi import APIRouter, Depends, Query
from pymongo.database import Database
from app.database import get_db
from app.schemas import GrupoEstatistica

router = APIRouter(prefix='/estatisticas', tags=['Estatísticas'])


def agrupar_por(db: Database, campo: str, uf: str | None, limite: int):
    filtro: dict = {campo: {'$type': 'string', '$ne': ''}}
    if uf:
        filtro['uf'] = uf.upper()
    pipeline = [
        {'$match': filtro},
        {'$group': {'_id': f'${campo}', 'total_candidaturas': {'$sum': 1}}},
        {'$sort': {'_id': 1}},
        {'$limit': limite},
        {'$project': {'_id': 0, 'valor': '$_id', 'total_candidaturas': 1}},
    ]
    return list(db.candidatos.aggregate(pipeline))


@router.get('/municipios', response_model=list[GrupoEstatistica])
def por_municipio(
    uf: str | None = Query(default='CE', min_length=2, max_length=2),
    limite: int = Query(default=200, ge=1, le=1000),
    db: Database = Depends(get_db),
):
    return agrupar_por(db, 'municipio', uf, limite)


@router.get('/partidos', response_model=list[GrupoEstatistica])
def por_partido(
    uf: str | None = Query(default='CE', min_length=2, max_length=2),
    limite: int = Query(default=100, ge=1, le=1000),
    db: Database = Depends(get_db),
):
    return agrupar_por(db, 'partido', uf, limite)


@router.get('/cargos', response_model=list[GrupoEstatistica])
def por_cargo(
    uf: str | None = Query(default='CE', min_length=2, max_length=2),
    limite: int = Query(default=100, ge=1, le=1000),
    db: Database = Depends(get_db),
):
    return agrupar_por(db, 'cargo', uf, limite)


@router.get('/bens/tipos')
def bens_por_tipo(db: Database = Depends(get_db)):
    """Soma em centavos (inteiro) para evitar erros de ponto flutuante."""
    return list(db.bens.aggregate([
        {'$match': {'tipo_bem': {'$type': 'string'}}},
        {'$group': {'_id': '$tipo_bem', 'quantidade': {'$sum': 1},
                    'valor_total_centavos': {'$sum': '$valor_centavos'}}},
        {'$sort': {'_id': 1}},
        {'$project': {'_id': 0, 'tipo_bem': '$_id', 'quantidade': 1,
                      'valor_total_centavos': 1}},
    ]))


@router.get('/resumo')
def resumo_base(db: Database = Depends(get_db)):
    """Quantidades de documentos efetivamente carregados nas cinco coleções."""
    return {
        nome: db[nome].count_documents({})
        for nome in ('candidatos', 'bens', 'coligacoes', 'vagas', 'redes_sociais')
    }
