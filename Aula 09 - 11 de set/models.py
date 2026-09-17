from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ClubeCreate(BaseModel):
    id_clube: int = Field(gt=0)
    nome: str
    cidade: str | None = None
    fundacao: date | None = None


class ClubeUpdate(BaseModel):
    nome: str
    cidade: str | None = None
    fundacao: date | None = None


class MembroCreate(BaseModel):
    id_membro: int = Field(gt=0)
    nome: str
    email: str | None = None
    id_clube: int | None = None


class MembroUpdate(BaseModel):
    nome: str
    email: str | None = None
    id_clube: int | None = None


class CorpoCelesteCreate(BaseModel):
    id_corpo: int = Field(gt=0)
    nome: str
    tipo: str | None = None
    constelacao: str | None = None


class EquipamentoCreate(BaseModel):
    id_equipamento: int = Field(gt=0)
    modelo: str
    tipo: str | None = None
    fabricante: str | None = None


class LocalCreate(BaseModel):
    id_local: int = Field(gt=0)
    nome: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    altitude_m: int | None = None


class EventoCreate(BaseModel):
    id_evento: int = Field(gt=0)
    titulo: str
    data_evento: date | None = None
    id_local: int | None = None


class OrganizacaoEventoCreate(BaseModel):
    id_evento: int
    id_clube: int


class ObservacaoCreate(BaseModel):
    id_obs: int = Field(gt=0)
    id_membro: int
    id_evento: int
    id_corpo: int
    id_equipamento: int
    horario: datetime
    condicoes_climaticas: str | None = None
    anotacoes: str | None = None
