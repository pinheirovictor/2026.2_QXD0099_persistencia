from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlmodel import Session, select

from app.database import getSession
from app.models import Consulta, Especialidade, Medico, Paciente, StatusConsulta

router = APIRouter(prefix="/relatorios", tags=["Relatórios / Joins"])


@router.get("/agenda-detalhada")
def agenda_detalhada(
    session: Session = Depends(getSession),
    inicio: datetime | None = None,
    fim: datetime | None = None,
):
    statement = (
        select(
            Consulta.id,
            Consulta.data_hora,
            Consulta.status,
            Paciente.nome.label("paciente"),
            Medico.nome.label("medico"),
            Especialidade.nome.label("especialidade"),
            Consulta.valor,
        )
        .join(Paciente, Paciente.id == Consulta.paciente_id)
        .join(Medico, Medico.id == Consulta.medico_id)
        .join(Especialidade, Especialidade.id == Consulta.especialidade_id)
    )

    if inicio:
        statement = statement.where(Consulta.data_hora >= inicio)

    if fim:
        statement = statement.where(Consulta.data_hora <= fim)

    statement = statement.order_by(Consulta.data_hora)

    rows = session.exec(statement).all()

    return [
        {
            "id": row.id,
            "data_hora": row.data_hora,
            "status": row.status,
            "paciente": row.paciente,
            "medico": row.medico,
            "especialidade": row.especialidade,
            "valor": row.valor,
        }
        for row in rows
    ]


@router.get("/consultas-por-medico")
def consultas_por_medico(session: Session = Depends(getSession)):
    statement = (
        select(
            Medico.id,
            Medico.nome,
            func.count(Consulta.id).label("quantidade_consultas"),
        )
        .outerjoin(Consulta, Consulta.medico_id == Medico.id)
        .group_by(Medico.id, Medico.nome)
        .order_by(func.count(Consulta.id).desc())
    )

    rows = session.exec(statement).all()

    return [
        {
            "medico_id": row.id,
            "medico": row.nome,
            "quantidade_consultas": row.quantidade_consultas,
        }
        for row in rows
    ]


@router.get("/consultas-por-especialidade")
def consultas_por_especialidade(session: Session = Depends(getSession)):
    statement = (
        select(
            Especialidade.nome,
            func.count(Consulta.id).label("quantidade"),
        )
        .outerjoin(Consulta, Consulta.especialidade_id == Especialidade.id)
        .group_by(Especialidade.id, Especialidade.nome)
        .order_by(func.count(Consulta.id).desc())
    )

    rows = session.exec(statement).all()

    return [
        {
            "especialidade": row.nome,
            "quantidade_consultas": row.quantidade,
        }
        for row in rows
    ]


@router.get("/faturamento-por-medico")
def faturamento_por_medico(session: Session = Depends(get_session)):
    statement = (
        select(
            Medico.id,
            Medico.nome,
            func.count(Consulta.id).label("quantidade"),
            func.coalesce(func.sum(Consulta.valor), 0).label("faturamento"),
        )
        .outerjoin(
            Consulta,
            (Consulta.medico_id == Medico.id)
            & (Consulta.status == StatusConsulta.REALIZADA),
        )
        .group_by(Medico.id, Medico.nome)
        .order_by(func.coalesce(func.sum(Consulta.valor), 0).desc())
    )

    rows = session.exec(statement).all()

    return [
        {
            "medico_id": row.id,
            "medico": row.nome,
            "consultas_realizadas": row.quantidade,
            "faturamento": float(row.faturamento),
        }
        for row in rows
    ]


@router.get("/pacientes-mais-atendidos")
def pacientes_mais_atendidos(session: Session = Depends(getSession)):
    statement = (
        select(
            Paciente.id,
            Paciente.nome,
            func.count(Consulta.id).label("quantidade"),
        )
        .join(Consulta, Consulta.paciente_id == Paciente.id)
        .group_by(Paciente.id, Paciente.nome)
        .order_by(func.count(Consulta.id).desc())
        .limit(10)
    )

    rows = session.exec(statement).all()

    return [
        {
            "paciente_id": row.id,
            "paciente": row.nome,
            "quantidade_consultas": row.quantidade,
        }
        for row in rows
    ]
