"""Modelos Pydantic: contratos públicos da API (sem CPF ou título eleitoral)."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CandidatoCriacao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1, max_length=200)
    municipio: str = Field(min_length=1, max_length=120)
    cargo: str = Field(min_length=1, max_length=100)
    partido: str = Field(min_length=1, max_length=30)
    nome_urna: str | None = None
    numero: str | None = None
    uf: str = Field(default="CE", min_length=2, max_length=2)
    ano: int = Field(default=2024, ge=1900, le=2100)
    situacao: str | None = None


class CandidatoAtualizacao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str | None = Field(default=None, min_length=1, max_length=200)
    municipio: str | None = Field(default=None, min_length=1, max_length=120)
    cargo: str | None = Field(default=None, min_length=1, max_length=100)
    partido: str | None = Field(default=None, min_length=1, max_length=30)
    nome_urna: str | None = None
    numero: str | None = None
    uf: str | None = Field(default=None, min_length=2, max_length=2)
    ano: int | None = Field(default=None, ge=1900, le=2100)
    situacao: str | None = None


class CandidatoLeitura(BaseModel):
    id: str
    nome: str
    municipio: str
    cargo: str
    partido: str
    origem: Literal["tse", "manual"]
    nome_urna: str | None = None
    numero: str | None = None
    uf: str | None = None
    ano: int | None = None
    situacao: str | None = None
    sq_candidato: str | None = None
    sq_coligacao: str | None = None
    cd_eleicao: str | None = None
    turno: int | None = None
    numero_partido: str | None = None


class PaginaCandidatos(BaseModel):
    total: int
    pagina: int
    limite: int
    total_paginas: int
    dados: list[CandidatoLeitura]


class GrupoEstatistica(BaseModel):
    valor: str
    total_candidaturas: int


def serializar_candidato(documento: dict) -> dict:
    """Retira o nome interno `_id` da resposta, exibindo `id`."""
    return {"id": str(documento["_id"]), **{
        chave: valor for chave, valor in documento.items() if chave != "_id"
    }}
