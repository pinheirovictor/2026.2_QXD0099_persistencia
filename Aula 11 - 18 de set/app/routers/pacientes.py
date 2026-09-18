from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import getSession
from models import(
    Paciente,
    PacienteCreate,
    PacientePublic,
    PacienteUpdate,
    PaginaPacientes,
    MetadadosPaginacao
)

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


@router.post("/", response_model=PacientePublic, status_code=201,)
def criar_paciente(dados: PacienteCreate, session: Session = Depends(getSession),):
    paciente = Paciente.model_validate(dados)
    session.add(paciente)
    
    try:
        session.commit()
        session.refresh(paciente)
        return paciente
    except IntegrityError:
        session.rollback()
        
        raise HTTPException(
            status_code=409,
            detail="CPF já cadastrado"
        )
        
@router.get("/", response_model=PaginaPacientes)
def listar_pacientes(
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10, ge=1, le=100, description="QTD registros por página"),
    nome: str = Query (default=None, description="Filtar pelo nome"),
    ativo: bool = Query(default=None, description="Filtro pelo status de ativo ou inativo"),
    session: Session = Depends(getSession),
):
    consulta = select(Paciente)
    
    consulta_total = (
        select(func.count()).select_from(Paciente)
    )
    
    if nome:
        filtro_nome = Paciente.nome.ilike(
            f"%{nome}%"
        )
        consulta = consulta.where(
            filtro_nome
        )
        
        consulta_total = consulta_total.where(
            filtro_nome
        )
    
    if ativo is not None:
        filtro_ativo = (
            Paciente.ativo == ativo
        )
        
        consulta = consulta.where(
            filtro_ativo
        )
        
        consulta_total = consulta_total.where(
            filtro_ativo
        )
    
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
        consulta
        .order_by(Paciente.nome)
        .offset(deslocamento)
        .limit(tamanho_pagina)
    )
    
    pacintes = session.exec(
        consulta
    ).all()
    
    return PaginaPacientes(
        dados=pacintes,
        paginacao= MetadadosPaginacao(
            total_registros=total_registros,
            total_paginas=total_paginas,
            pagina_atual=pagina,
            tamanho_pagina=tamanho_pagina,
        )
    )
    
    
    