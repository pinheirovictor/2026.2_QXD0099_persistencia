"""Relacionamentos documentais por chave e junções $lookup."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.database import Database
from app.database import get_db
from app.schemas import serializar_candidato

router = APIRouter(prefix='/candidatos', tags=['Relacionamentos ($lookup)'])


def obter_candidato(db, id_candidato):
    candidato = db.candidatos.find_one({'_id': id_candidato})
    if candidato is None:
        raise HTTPException(404, detail='Candidatura não encontrada')
    return candidato


@router.get('/{id_candidato}/bens')
def bens_do_candidato(
    id_candidato: str,
    limite: int = Query(100, ge=1, le=500),
    db: Database = Depends(get_db),
):
    candidato = obter_candidato(db, id_candidato)
    chave = candidato.get('chave_candidato')
    resultados = db.bens.find({'chave_candidato': chave}).sort('ordem', 1).limit(limite) if chave else []
    return [serializar_candidato(doc) for doc in resultados]


@router.get('/{id_candidato}/redes-sociais')
def redes_do_candidato(
    id_candidato: str,
    limite: int = Query(100, ge=1, le=500),
    db: Database = Depends(get_db),
):
    candidato = obter_candidato(db, id_candidato)
    chave = candidato.get('chave_candidato')
    resultados = db.redes_sociais.find({'chave_candidato': chave}).sort('ordem', 1).limit(limite) if chave else []
    return [serializar_candidato(doc) for doc in resultados]


@router.get('/{id_candidato}/detalhes')
def detalhes_candidato(id_candidato: str, db: Database = Depends(get_db)):
    """Join entre cinco coleções usando $lookup (apenas registros oficiais)."""
    obter_candidato(db, id_candidato)
    pipeline = [
        {'$match': {'_id': id_candidato}},
        {'$lookup': {'from': 'bens', 'localField': 'chave_candidato',
                     'foreignField': 'chave_candidato', 'as': 'bens'}},
        {'$lookup': {'from': 'redes_sociais', 'localField': 'chave_candidato',
                     'foreignField': 'chave_candidato', 'as': 'redes_sociais'}},
        {'$lookup': {'from': 'coligacoes', 'localField': 'chave_coligacao',
                     'foreignField': 'chave_coligacao', 'as': 'coligacoes'}},
        {'$lookup': {'from': 'vagas', 'localField': 'chave_vaga',
                     'foreignField': 'chave_vaga', 'as': 'vagas'}},
    ]
    resultado = next(iter(db.candidatos.aggregate(pipeline)), None)
    if resultado is None:
        raise HTTPException(404, detail='Candidatura não encontrada')
    # _id é sempre string nos cinco conjuntos importados.
    ligados = {
        nome: [serializar_candidato(x) for x in resultado.pop(nome, [])]
        for nome in ('bens', 'redes_sociais', 'coligacoes', 'vagas')
    }
    return {'candidato': serializar_candidato(resultado), **ligados}
