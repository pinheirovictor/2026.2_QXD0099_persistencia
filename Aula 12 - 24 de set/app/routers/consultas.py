from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlmodel import Session, select

from database import getSession
from models import (
    Consulta,
    ConsultaCreate,
    ConsultaPublic,
    ConsultaPublicDetalhada,
    ConsultaUpdate,
    Especialidade,
    Medico,
    MetadadosPaginacao,
    Paciente,
    PaginaConsultas,
    StatusConsulta,
)

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"],
)

def validar_referencias(
    paciente_id: int,
    medico_id: int,
    especialidade_id: int,
    session: Session
):
    paciente = session.get(
        Paciente,
        paciente_id
    )
    
    medico = session.get(
        Medico,
        medico_id
    )
    
    especialidade = session.get(
        Especialidade,
        especialidade_id
    )
    
    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado"
        )
        
    if not medico:
        raise HTTPException(
            status_code=404,
            detail="Medico não encontrado"
        )
        
    if not especialidade:
        raise HTTPException(
            status_code=404,
            detail="Especialidade não encontrada"
        )
        
    if especialidade not in medico.especialidades:
        raise HTTPException(
            status_code=400,
            detail="O médico não está vinculado a esta especialidade"
        )
        
        
@router.post("/", response_model=ConsultaPublic, status_code=201)
def criar_consulta(dados: ConsultaCreate, session: Session = Depends(getSession)):
    validar_referencias(
        dados.paciente_id,
        dados.medico_id,
        dados.especlidade_id,
        session
    )
    
    conflito = session.exec(
        select(Consulta).where(
            Consulta.medico_id == dados.medico_id,
            Consulta.data_hora == dados.data_hora,
            Consulta.status != StatusConsulta.CANCELADA
        )
    ).first()
    
    if conflito:
        raise HTTPException(
            status_code=409,
            detail="O médico já possui uma consulta neste horário"
            )
    
    consulta = Consulta.model_validate(
        dados
    )
    
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    
    return consulta
    
    
@router.get("/", response_model=PaginaConsultas)
def listar_consultas(
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

    paciente_id: int | None = Query(
        default=None,
        description="Filtra as consultas pelo paciente.",
    ),

    medico_id: int | None = Query(
        default=None,
        description="Filtra as consultas pelo médico.",
    ),

    especialidade_id: int | None = Query(
        default=None,
        description="Filtra as consultas pela especialidade.",
    ),

    status: StatusConsulta | None = Query(
        default=None,
        description="Filtra as consultas pelo status.",
    ),

    inicio: datetime | None = Query(
        default=None,
        description="Data e hora inicial do período.",
    ),

    fim: datetime | None = Query(
        default=None,
        description="Data e hora final do período.",
    ),

    session: Session = Depends(getSession),
):
    consulta = select(Consulta)
    
    consulta_total = (
        select(func.count())
        .select_from(Consulta)
    )
    
    if paciente_id is not None:
        filtro_paciente = (
            Consulta.paciente_id == paciente_id
        )
    
        consulta = consulta.where(filtro_paciente)
        
        consulta_total = consulta_total.where(filtro_paciente)
    
    if medico_id is not None:
        filtro_medico = (
            Consulta.medico_id == medico_id
        )
    
        consulta = consulta.where(filtro_medico)
        
        consulta_total = consulta_total.where(filtro_medico)
        
    if especialidade_id is not None:
        filtro_especialidade = (
            Consulta.especlidade_id == especialidade_id
        )
    
        consulta = consulta.where(filtro_especialidade)
        
        consulta_total = consulta_total.where(filtro_especialidade)
        
    if status is not None:
        filtro_status = (
            Consulta.status == status
        )
    
        consulta = consulta.where(filtro_status)
        
        consulta_total = consulta_total.where(filtro_status)
        
    if inicio is not None:
        filtro_inicio = (
            Consulta.data_hora >= inicio
        )
    
        consulta = consulta.where(filtro_inicio)
        
        consulta_total = consulta_total.where(filtro_inicio)
        
    if fim is not None:
        filtro_fim = (
            Consulta.data_hora <= fim
        )
    
        consulta = consulta.where(filtro_fim)
        
        consulta_total = consulta_total.where(filtro_fim)
        
    total_registros = session.exec(
        consulta_total
    ).one()
    
    total_paginas = (
        total_registros + tamanho_pagina - 1
    ) // tamanho_pagina
    
    
    deslocamento = (
        pagina - 1
    ) * tamanho_pagina
    
    consulta = (
        consulta.order_by(
            Consulta.data_hora.desc()
        )
        .offset(deslocamento)
        .limit(tamanho_pagina)
    )
    
    consultas = session.exec(
        consulta
    ).all()
    
    return PaginaConsultas(
        dados=consultas,
        
        paginacao=MetadadosPaginacao(
            total_registros=total_registros,
            total_paginas=total_paginas,
            pagina_atual=pagina,
            tamanho_pagina=tamanho_pagina
        )
    )
