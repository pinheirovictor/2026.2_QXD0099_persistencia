from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import getSession
from models import (
    Especialidade,
    EspecialidadeCreate,
    EspecialidadePublic,
    EspecialidadeUpdate,
    MetadadosPaginacao,
    PaginaEspecialidades,
)

router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"],
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=EspecialidadePublic,
    status_code=201,
)
def criar_especialidade(
    dados: EspecialidadeCreate,
    session: Session = Depends(getSession),
):
    especialidade = Especialidade.model_validate(
        dados
    )

    session.add(
        especialidade
    )

    try:
        session.commit()
        session.refresh(especialidade)

        return especialidade

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Especialidade já cadastrada.",
        )


# =========================================================
# READ - LISTAGEM COM PAGINAÇÃO
# =========================================================

@router.get(
    "/",
    response_model=PaginaEspecialidades,
)
def listar_especialidades(
    pagina: int = Query(
        1,
        ge=1,
        description="Número da página.",
    ),

    tamanho_pagina: int = Query(
        10,
        ge=1,
        le=100,
        description="Quantidade de registros por página.",
    ),

    nome: str | None = Query(
        default=None,
        description="Filtra especialidades pelo nome.",
    ),

    session: Session = Depends(getSession),
):
    # -----------------------------------------------------
    # Consulta principal
    # -----------------------------------------------------

    consulta = select(
        Especialidade
    )

    # -----------------------------------------------------
    # Consulta para contar o total de registros
    # -----------------------------------------------------

    consulta_total = (
        select(func.count())
        .select_from(Especialidade)
    )

    # -----------------------------------------------------
    # Filtro por nome
    # -----------------------------------------------------

    if nome:
        filtro_nome = (
            Especialidade.nome.ilike(
                f"%{nome}%"
            )
        )

        consulta = consulta.where(
            filtro_nome
        )

        consulta_total = consulta_total.where(
            filtro_nome
        )

    # -----------------------------------------------------
    # Total de registros
    # -----------------------------------------------------

    total_registros = session.exec(
        consulta_total
    ).one()

    # -----------------------------------------------------
    # Total de páginas
    # -----------------------------------------------------

    total_paginas = (
        total_registros
        + tamanho_pagina
        - 1
    ) // tamanho_pagina

    # -----------------------------------------------------
    # Cálculo do deslocamento
    # -----------------------------------------------------

    deslocamento = (
        pagina - 1
    ) * tamanho_pagina

    # -----------------------------------------------------
    # Ordenação + paginação
    # -----------------------------------------------------

    consulta = (
        consulta
        .order_by(
            Especialidade.nome
        )
        .offset(
            deslocamento
        )
        .limit(
            tamanho_pagina
        )
    )

    especialidades = session.exec(
        consulta
    ).all()

    # -----------------------------------------------------
    # Resposta
    # -----------------------------------------------------

    return PaginaEspecialidades(
        dados=especialidades,

        paginacao=MetadadosPaginacao(
            total_registros=total_registros,
            total_paginas=total_paginas,
            pagina_atual=pagina,
            tamanho_pagina=tamanho_pagina,
        ),
    )


# =========================================================
# READ - BUSCAR POR ID
# =========================================================

@router.get(
    "/{especialidade_id}",
    response_model=EspecialidadePublic,
)
def buscar_especialidade(
    especialidade_id: int,
    session: Session = Depends(getSession),
):
    especialidade = session.get(
        Especialidade,
        especialidade_id,
    )

    if not especialidade:
        raise HTTPException(
            status_code=404,
            detail="Especialidade não encontrada.",
        )

    return especialidade


# =========================================================
# UPDATE
# =========================================================

@router.patch(
    "/{especialidade_id}",
    response_model=EspecialidadePublic,
)
def atualizar_especialidade(
    especialidade_id: int,
    dados: EspecialidadeUpdate,
    session: Session = Depends(getSession),
):
    especialidade = session.get(
        Especialidade,
        especialidade_id,
    )

    if not especialidade:
        raise HTTPException(
            status_code=404,
            detail="Especialidade não encontrada.",
        )

    dados_atualizacao = dados.model_dump(
        exclude_unset=True
    )

    especialidade.sqlmodel_update(
        dados_atualizacao
    )

    session.add(
        especialidade
    )

    try:
        session.commit()
        session.refresh(
            especialidade
        )

        return especialidade

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Especialidade já cadastrada.",
        )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{especialidade_id}",
    status_code=204,
)
def excluir_especialidade(
    especialidade_id: int,
    session: Session = Depends(getSession),
):
    especialidade = session.get(
        Especialidade,
        especialidade_id,
    )

    if not especialidade:
        raise HTTPException(
            status_code=404,
            detail="Especialidade não encontrada.",
        )

    session.delete(
        especialidade
    )

    try:
        session.commit()

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Especialidade possui vínculos "
                "e não pode ser removida."
            ),
        )