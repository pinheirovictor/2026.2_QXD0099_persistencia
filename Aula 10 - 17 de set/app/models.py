from datetime import date, datetime
from enum import Enum
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class StatusConsulta(str, Enum):
    AGENDADA = "agendada"
    CONFIRMADA = "confirmada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
    
# MedicoEspecialidade

class MedicoEspecialidade(SQLModel, table=True):
    medico_id: int | None = Field(
        default=None,
        foreign_key="medico.id",
        primary_key=True,
    )
    especialidade_id: int | None = Field(
        default=None,
        foreign_key="especialidade.id",
        primary_key=True,
    )


# Paciente

class PacienteBase(SQLModel):
    nome: str = Field(min_length=3, max_length=120, index=True)
    cpf: str = Field(
        sa_column=Column(
            String(14), 
            unique=True, 
            nullable=False,
            index=True
        )
    )
    data_nascimento: date
    email: str | None = Field(default=None, unique=True, max_length=120)
    telefone: str | None = Field(default=None, max_length=20)
    ativo: bool = True
    
class Paciente(PacienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # voltamos já, para fazer o relacionamento
    
class PacienteCreate(PacienteBase):
    pass

class PacientePublic(PacienteBase):
    id: int
    
class PacienteUpdate(SQLModel):
    nome: str = Field(min_length=3, max_length=120, index=True)
    cpf: str | None = None
    data_nascimento: date | None = None
    email: str | None = None
    telefone: str | None = None
    ativo: bool | None = None
    
# Especilidade

class EspecilidadeBase(SQLModel):
    nome: str = Field(min_length=3, 
                      max_length=120, 
                      index=True, 
                      nullable=False, 
                      unique=True)
    descricao: str | None = Field(default=None, max_length=300)
    
class Especialidade(EspecilidadeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
     
    # voltamos já, para fazer o relacionamento
    medicos: list["Medico"] = Relationship(
        back_populates="especialidades",
        link_model=MedicoEspecialidade
    )
    
class EspecialidadeCreate(EspecilidadeBase):
    pass

class EspecialidadePublic(EspecilidadeBase):
    id: int 

class EspecialidadeUpdate(SQLModel):
    nome: str | None = None
    descricao: str | None = None
    
# Médico

class MedicoBase(SQLModel):
    nome: str = Field(min_length=3, max_length=120, index=True)
    crm: str = Field(
        sa_column=Column(
            String(30),
            unique=True,
            nullable=False, 
            index=True
        )
    )
    email: str | None = Field(default=None, unique=True, max_length=120)
    telefone: str | None = Field(default=None, max_length=20)
    ativo: bool = True
    
class Medico(MedicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
     
    # voltamos já, para fazer o relacionamento
    especialidades: list[Especialidade] = Relationship(
        back_populates="medicos",
        link_model=MedicoEspecialidade
    )
    
class MedicoCreate(MedicoBase):
    pass 

class MedicoPublic(MedicoBase):
    id: int
    
class MedicoPublicDetalhado(MedicoPublic):
    especialidade: list[Especialidade] = []
    
class MedicoUpdate(SQLModel):
    nome: str | None = None
    crm: str | None = None
    email: str | None = None
    telefone: str | None = None
    ativo: bool | None = None
    especialidade_ids: list[int] | None = None
    
class ConsultaBase(SQLModel):
    paciente_id: int = Field(foreign_key="paciente.id", index=True)
    medico_id: int = Field(foreign_key="medico.id", index=True)
    especlidade_id: int = Field(foreign_key="especialidade.id", index=True)
    
    data_hora: datetime = Field(index=True)
    status: StatusConsulta = Field(default=StatusConsulta.AGENDADA, index=True)
    motivo: str = Field(min_length=3, max_length=300)
    observacoes: str | None = Field(default=None, min_length=3, max_length=1000)
    valor: float = Field(default=0, ge=0)
    
class Consultas(ConsultaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    paciente: Paciente | None = Relationship(back_populates="consultas")
    medico: Medico | None = Relationship(back_populates="consultas")
    especialidade: Especialidade | None = Relationship(back_populates="consultas")
    
class ConsultaCreate(ConsultaBase):
    pass 

class ConsultaPublic(ConsultaBase):
    id: int
    
class ConsultaPublicDetalhada(ConsultaPublic):
    paciente: PacientePublic | None = None
    medico: MedicoPublic | None = None
    especilidade: EspecialidadePublic | None = None
    
