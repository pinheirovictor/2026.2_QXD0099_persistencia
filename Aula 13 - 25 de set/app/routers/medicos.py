from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import getSession
from models import (
    Especialidade,
    Medico,
    MedicoCreate,
    MedicoPublic,
    MedicoPublicDetalhado,
    MedicoUpdate,
    MetadadosPaginacao,
    PaginaMedicos,
)

router = APIRouter(
    prefix="/medicos",
    tags=["Médicos"],
)


# =========================================================
# FUNÇÃO AUXILIAR - OBTER ESPECIALIDADES
# =========================================================

def obter_especialidades(
    ids: list[int],
    session: Session,
) -> list[Especialidade]:

    especialidades = []

    for especialidade_id in set(ids):
        especialidade = session.get(
            Especialidade,
            especialidade_id,
        )

        if not especialidade:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Especialidade {especialidade_id} "
                    "não encontrada."
                ),
            )

        especialidades.append(
            especialidade
        )

    return especialidades


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=MedicoPublicDetalhado,
    status_code=201,
)
def criar_medico(
    dados: MedicoCreate,
    session: Session = Depends(getSession),
):
    # -----------------------------------------------------
    # Busca as especialidades informadas
    # -----------------------------------------------------

    especialidades = obter_especialidades(
        dados.especialidade_ids,
        session,
    )

    # -----------------------------------------------------
    # Criação do médico
    # -----------------------------------------------------

    medico = Medico(
        **dados.model_dump(
            exclude={"especialidade_ids"}
        ),
        especialidades=especialidades,
    )

    session.add(medico)

    try:
        session.commit()
        session.refresh(medico)

        return medico

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="CRM já cadastrado.",
        )


# =========================================================
# READ - LISTAGEM COM FILTROS E PAGINAÇÃO
# =========================================================

@router.get(
    "/",
    response_model=PaginaMedicos,
)
def listar_medicos(
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
        description="Filtra médicos pelo nome.",
    ),

    especialidade_id: int | None = Query(
        default=None,
        description="Filtra médicos por especialidade.",
    ),

    session: Session = Depends(getSession),
):
    # -----------------------------------------------------
    # Consulta principal
    # -----------------------------------------------------

    consulta = select(Medico)

    # -----------------------------------------------------
    # Consulta para contar o total de registros
    # -----------------------------------------------------

    consulta_total = (
        select(
            func.count(
                func.distinct(Medico.id)
            )
        )
        .select_from(Medico)
    )

    # -----------------------------------------------------
    # Filtro por nome
    # -----------------------------------------------------

    if nome:
        filtro_nome = Medico.nome.ilike(
            f"%{nome}%"
        )

        consulta = consulta.where(
            filtro_nome
        )

        consulta_total = consulta_total.where(
            filtro_nome
        )

    # -----------------------------------------------------
    # Filtro por especialidade
    # -----------------------------------------------------

    if especialidade_id is not None:

        consulta = (
            consulta
            .join(Medico.especialidades)
            .where(
                Especialidade.id
                == especialidade_id
            )
        )

        consulta_total = (
            consulta_total
            .join(Medico.especialidades)
            .where(
                Especialidade.id
                == especialidade_id
            )
        )

    # -----------------------------------------------------
    # Total de registros encontrados
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
        .order_by(Medico.nome)
        .offset(deslocamento)
        .limit(tamanho_pagina)
    )

    medicos = session.exec(
        consulta
    ).all()

    # -----------------------------------------------------
    # Resposta
    # -----------------------------------------------------

    return PaginaMedicos(
        dados=medicos,

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
    "/{medico_id}",
    response_model=MedicoPublicDetalhado,
)
def buscar_medico(
    medico_id: int,
    session: Session = Depends(getSession),
):
    medico = session.get(
        Medico,
        medico_id,
    )

    if not medico:
        raise HTTPException(
            status_code=404,
            detail="Médico não encontrado.",
        )

    return medico


# =========================================================
# UPDATE
# =========================================================

@router.patch(
    "/{medico_id}",
    response_model=MedicoPublicDetalhado,
)
def atualizar_medico(
    medico_id: int,
    dados: MedicoUpdate,
    session: Session = Depends(getSession),
):
    medico = session.get(
        Medico,
        medico_id,
    )

    if not medico:
        raise HTTPException(
            status_code=404,
            detail="Médico não encontrado.",
        )

    # -----------------------------------------------------
    # Dados enviados para atualização
    # -----------------------------------------------------

    valores = dados.model_dump(
        exclude_unset=True
    )

    # -----------------------------------------------------
    # Remove especialidade_ids dos campos simples
    # -----------------------------------------------------

    especialidade_ids = valores.pop(
        "especialidade_ids",
        None,
    )

    # -----------------------------------------------------
    # Atualiza dados básicos
    # -----------------------------------------------------

    medico.sqlmodel_update(
        valores
    )

    # -----------------------------------------------------
    # Atualiza especialidades, caso informadas
    # -----------------------------------------------------

    if especialidade_ids is not None:

        medico.especialidades = (
            obter_especialidades(
                especialidade_ids,
                session,
            )
        )

    session.add(medico)

    try:
        session.commit()
        session.refresh(medico)

        return medico

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="CRM já cadastrado.",
        )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{medico_id}",
    status_code=204,
)
def excluir_medico(
    medico_id: int,
    session: Session = Depends(getSession),
):
    medico = session.get(
        Medico,
        medico_id,
    )

    if not medico:
        raise HTTPException(
            status_code=404,
            detail="Médico não encontrado.",
        )

    session.delete(medico)

    try:
        session.commit()

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Médico possui consultas associadas "
                "e não pode ser removido."
            ),
        )