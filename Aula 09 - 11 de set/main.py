import psycopg2
from fastapi import FastAPI, HTTPException, status

import crud
from models import (
    ClubeCreate,
    ClubeUpdate,
    MembroCreate,
    MembroUpdate,
    CorpoCelesteCreate,
    EquipamentoCreate,
    LocalCreate,
    EventoCreate,
    OrganizacaoEventoCreate,
    ObservacaoCreate,
)


app = FastAPI(
    title="API de Astronomia",
    description="FastAPI + DB-API + PostgreSQL, sem ORM.",
    version="1.0.0",
)


def erro_404(recurso):
    raise HTTPException(
        status_code=404,
        detail=f"{recurso} não encontrado.",
    )


# ============================================================
# CRUD COMPLETO - CLUBE
# ============================================================

@app.post("/clubes", status_code=201, tags=["Clubes"])
def criar_clube(dados: ClubeCreate):
    try:
        return crud.criar_clube(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail="Já existe um clube com esse ID.",
        ) from erro


@app.get("/clubes", tags=["Clubes"])
def listar_clubes():
    return crud.listar_clubes()


@app.get("/clubes/{id_clube}", tags=["Clubes"])
def buscar_clube(id_clube: int):
    clube = crud.buscar_clube(id_clube)

    if clube is None:
        erro_404("Clube")

    return clube


@app.put("/clubes/{id_clube}", tags=["Clubes"])
def atualizar_clube(
    id_clube: int,
    dados: ClubeUpdate,
):
    clube = crud.atualizar_clube(
        id_clube,
        dados,
    )

    if clube is None:
        erro_404("Clube")

    return clube


@app.delete("/clubes/{id_clube}", tags=["Clubes"])
def excluir_clube(id_clube: int):
    try:
        clube = crud.excluir_clube(
            id_clube
        )
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail=(
                "O clube não pode ser removido "
                "porque possui registros relacionados."
            ),
        ) from erro

    if clube is None:
        erro_404("Clube")

    return {
        "mensagem": "Clube excluído.",
        "registro": clube,
    }


# ============================================================
# CRUD COMPLETO - MEMBRO
# ============================================================

@app.post("/membros", status_code=201, tags=["Membros"])
def criar_membro(dados: MembroCreate):
    try:
        return crud.criar_membro(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail=(
                "ID duplicado ou clube informado não existe."
            ),
        ) from erro


@app.get("/membros", tags=["Membros"])
def listar_membros():
    return crud.listar_membros()


@app.get("/membros/{id_membro}", tags=["Membros"])
def buscar_membro(id_membro: int):
    membro = crud.buscar_membro(
        id_membro
    )

    if membro is None:
        erro_404("Membro")

    return membro


@app.put("/membros/{id_membro}", tags=["Membros"])
def atualizar_membro(
    id_membro: int,
    dados: MembroUpdate,
):
    try:
        membro = crud.atualizar_membro(
            id_membro,
            dados,
        )
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail="O clube informado não existe.",
        ) from erro

    if membro is None:
        erro_404("Membro")

    return membro


@app.delete("/membros/{id_membro}", tags=["Membros"])
def excluir_membro(id_membro: int):
    try:
        membro = crud.excluir_membro(
            id_membro
        )
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail=(
                "O membro possui observações relacionadas."
            ),
        ) from erro

    if membro is None:
        erro_404("Membro")

    return {
        "mensagem": "Membro excluído.",
        "registro": membro,
    }


# ============================================================
# DEMAIS TABELAS
# ============================================================

@app.post("/corpos", status_code=201, tags=["Corpos Celestes"])
def criar_corpo(dados: CorpoCelesteCreate):
    try:
        return crud.criar_corpo(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(409, "ID já cadastrado.") from erro


@app.get("/corpos", tags=["Corpos Celestes"])
def listar_corpos():
    return crud.listar_corpos()


@app.post("/equipamentos", status_code=201, tags=["Equipamentos"])
def criar_equipamento(dados: EquipamentoCreate):
    try:
        return crud.criar_equipamento(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(409, "ID já cadastrado.") from erro


@app.get("/equipamentos", tags=["Equipamentos"])
def listar_equipamentos():
    return crud.listar_equipamentos()


@app.post("/locais", status_code=201, tags=["Locais"])
def criar_local(dados: LocalCreate):
    try:
        return crud.criar_local(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(409, "ID já cadastrado.") from erro


@app.get("/locais", tags=["Locais"])
def listar_locais():
    return crud.listar_locais()


@app.post("/eventos", status_code=201, tags=["Eventos"])
def criar_evento(dados: EventoCreate):
    try:
        return crud.criar_evento(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            409,
            "ID duplicado ou local inexistente."
        ) from erro


@app.get("/eventos", tags=["Eventos"])
def listar_eventos():
    return crud.listar_eventos()


# ============================================================
# RELAÇÃO N:M
# ============================================================

@app.post("/organizacoes", status_code=201, tags=["Organização"])
def organizar_evento(
    dados: OrganizacaoEventoCreate
):
    try:
        return crud.organizar_evento(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            409,
            "Evento/clube inexistente ou associação duplicada."
        ) from erro


@app.get(
    "/eventos/{id_evento}/clubes",
    tags=["Organização"],
)
def clubes_do_evento(id_evento: int):
    return crud.listar_clubes_do_evento(
        id_evento
    )


# ============================================================
# OBSERVAÇÕES
# ============================================================

@app.post("/observacoes", status_code=201, tags=["Observações"])
def criar_observacao(
    dados: ObservacaoCreate
):
    try:
        return crud.criar_observacao(
            dados
        )
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            409,
            (
                "ID duplicado ou uma das chaves "
                "estrangeiras não existe."
            ),
        ) from erro


@app.get("/observacoes", tags=["Observações"])
def listar_observacoes():
    return crud.listar_observacoes()


@app.get("/estatisticas", tags=["Consultas SQL"])
def estatisticas():
    return crud.estatisticas_por_tipo_corpo()


@app.get("/", tags=["Sistema"])
def home():
    return {
        "mensagem": "API de Astronomia ativa.",
        "documentacao": "/docs",
    }
