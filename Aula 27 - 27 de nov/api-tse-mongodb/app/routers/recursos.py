"""Consultas paginadas às demais quatro coleções oficiais do TSE."""
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.database import Database
from app.database import get_db
from app.schemas import serializar_candidato

router = APIRouter(tags=["Dados oficiais"])


def exato(s: str) -> dict:
    return {"$regex": f"^{re.escape(s.strip())}$", "$options": "i"}


def pagina(db: Database, colecao: str, filtros: dict, n: int, limite: int) -> dict:
    total = db[colecao].count_documents(filtros)
    itens = db[colecao].find(filtros).sort('_id', 1).skip((n - 1) * limite).limit(limite)
    return {
        'total': total, 'pagina': n, 'limite': limite,
        'total_paginas': (total + limite - 1) // limite,
        'dados': [serializar_candidato(doc) for doc in itens],
    }


def detalhe(db: Database, colecao: str, id_registro: str) -> dict:
    doc = db[colecao].find_one({'_id': id_registro})
    if doc is None:
        raise HTTPException(404, detail='Registro não encontrado')
    return serializar_candidato(doc)


@router.get('/bens', tags=['Bens'])
def listar_bens(
    sq_candidato: str | None = None,
    municipio: str | None = None,
    tipo_bem: str | None = None,
    data_inicio: str | None = Query(None, pattern=r'^\d{4}-\d{2}-\d{2}$', description='Data inicial da atualização (YYYY-MM-DD)'),
    data_fim: str | None = Query(None, pattern=r'^\d{4}-\d{2}-\d{2}$', description='Data final da atualização (YYYY-MM-DD)'),
    pagina_atual: int = Query(1, alias='pagina', ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Database = Depends(get_db),
):
    filtros = {}
    if sq_candidato: filtros['sq_candidato'] = sq_candidato
    if municipio: filtros['municipio'] = exato(municipio)
    if tipo_bem: filtros['tipo_bem'] = exato(tipo_bem)
    if data_inicio or data_fim:
        filtros['data_atualizacao'] = {}
        if data_inicio: filtros['data_atualizacao']['$gte'] = data_inicio
        if data_fim: filtros['data_atualizacao']['$lte'] = data_fim
    return pagina(db, 'bens', filtros, pagina_atual, limite)


@router.get('/bens/{id_registro}', tags=['Bens'])
def consultar_bem(id_registro: str, db: Database = Depends(get_db)):
    return detalhe(db, 'bens', id_registro)


@router.get('/coligacoes', tags=['Coligações'])
def listar_coligacoes(
    municipio: str | None = None,
    partido: str | None = None,
    cargo: str | None = None,
    sq_coligacao: str | None = None,
    pagina_atual: int = Query(1, alias='pagina', ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Database = Depends(get_db),
):
    filtros = {}
    if municipio: filtros['municipio'] = exato(municipio)
    if partido: filtros['partido'] = exato(partido)
    if cargo: filtros['cargo'] = exato(cargo)
    if sq_coligacao: filtros['sq_coligacao'] = sq_coligacao
    return pagina(db, 'coligacoes', filtros, pagina_atual, limite)


@router.get('/coligacoes/{id_registro}', tags=['Coligações'])
def consultar_coligacao(id_registro: str, db: Database = Depends(get_db)):
    return detalhe(db, 'coligacoes', id_registro)


@router.get('/vagas', tags=['Vagas'])
def listar_vagas(
    municipio: str | None = None,
    cargo: str | None = None,
    pagina_atual: int = Query(1, alias='pagina', ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Database = Depends(get_db),
):
    filtros = {}
    if municipio: filtros['municipio'] = exato(municipio)
    if cargo: filtros['cargo'] = exato(cargo)
    return pagina(db, 'vagas', filtros, pagina_atual, limite)


@router.get('/vagas/{id_registro}', tags=['Vagas'])
def consultar_vaga(id_registro: str, db: Database = Depends(get_db)):
    return detalhe(db, 'vagas', id_registro)


@router.get('/redes-sociais', tags=['Redes sociais'])
def listar_redes_sociais(
    sq_candidato: str | None = None,
    dominio: str | None = None,
    pagina_atual: int = Query(1, alias='pagina', ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Database = Depends(get_db),
):
    filtros = {}
    if sq_candidato: filtros['sq_candidato'] = sq_candidato
    if dominio: filtros['dominio'] = exato(dominio)
    return pagina(db, 'redes_sociais', filtros, pagina_atual, limite)


@router.get('/redes-sociais/{id_registro}', tags=['Redes sociais'])
def consultar_rede_social(id_registro: str, db: Database = Depends(get_db)):
    return detalhe(db, 'redes_sociais', id_registro)
