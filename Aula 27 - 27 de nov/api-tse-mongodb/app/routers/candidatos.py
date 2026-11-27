"""Endpoints CRUD e consultas de candidaturas."""

import re
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.database import get_db
from app.schemas import (
    CandidatoAtualizacao,
    CandidatoCriacao,
    CandidatoLeitura,
    PaginaCandidatos,
    serializar_candidato,
)

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])


def filtro_exato(texto: str) -> dict:
    """Escapa caracteres especiais para a entrada não virar expressão regular."""
    return {"$regex": f"^{re.escape(texto.strip())}$", "$options": "i"}


@router.get("", response_model=PaginaCandidatos, summary="Listar candidaturas")
def listar_candidatos(
    municipio: str | None = Query(default=None, description="Ex.: QUIXADÁ"),
    cargo: str | None = None,
    partido: str | None = None,
    nome: str | None = None,
    origem: str | None = Query(default=None, pattern="^(tse|manual)$"),
    pagina: int = Query(default=1, ge=1),
    limite: int = Query(default=10, ge=1, le=100),
    db: Database = Depends(get_db),
):
    filtros: dict = {}
    if municipio:
        filtros["municipio"] = filtro_exato(municipio)
    if cargo:
        filtros["cargo"] = filtro_exato(cargo)
    if partido:
        filtros["partido"] = filtro_exato(partido)
    if nome:
        filtros["nome"] = {"$regex": re.escape(nome.strip()), "$options": "i"}
    if origem:
        filtros["origem"] = origem

    total = db.candidatos.count_documents(filtros)
    resultados = (
        db.candidatos.find(filtros)
        .sort([("nome", 1), ("_id", 1)])
        .skip((pagina - 1) * limite)
        .limit(limite)
    )
    return {
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "total_paginas": (total + limite - 1) // limite,
        "dados": [serializar_candidato(item) for item in resultados],
    }


@router.get("/{id_candidato}", response_model=CandidatoLeitura, summary="Consultar candidatura")
def consultar_candidato(id_candidato: str, db: Database = Depends(get_db)):
    documento = db.candidatos.find_one({"_id": id_candidato})
    if not documento:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    return serializar_candidato(documento)


@router.post(
    "",
    response_model=CandidatoLeitura,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar registro local (não altera dados do TSE)",
)
def criar_candidato(candidato: CandidatoCriacao, db: Database = Depends(get_db)):
    documento = candidato.model_dump()
    documento.update({"_id": f"local_{uuid4().hex}", "origem": "manual"})
    db.candidatos.insert_one(documento)
    return serializar_candidato(documento)


def exigir_registro_local(db: Database, id_candidato: str) -> dict:
    documento = db.candidatos.find_one({"_id": id_candidato})
    if documento is None:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    if documento.get("origem") != "manual":
        raise HTTPException(
            status_code=403,
            detail="Dados importados do TSE são somente leitura. Edite apenas registros locais.",
        )
    return documento


@router.patch("/{id_candidato}", response_model=CandidatoLeitura, summary="Atualizar registro local")
def atualizar_candidato(
    id_candidato: str,
    alteracoes: CandidatoAtualizacao,
    db: Database = Depends(get_db),
):
    exigir_registro_local(db, id_candidato)
    campos = alteracoes.model_dump(exclude_unset=True, exclude_none=True)
    if not campos:
        raise HTTPException(status_code=400, detail="Informe ao menos um campo para atualizar")
    db.candidatos.update_one({"_id": id_candidato, "origem": "manual"}, {"$set": campos})
    atualizado = db.candidatos.find_one({"_id": id_candidato})
    return serializar_candidato(atualizado)


@router.delete("/{id_candidato}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover registro local")
def excluir_candidato(id_candidato: str, db: Database = Depends(get_db)):
    exigir_registro_local(db, id_candidato)
    db.candidatos.delete_one({"_id": id_candidato, "origem": "manual"})
    return None
