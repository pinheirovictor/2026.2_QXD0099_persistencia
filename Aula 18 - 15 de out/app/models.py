from datetime import datetime

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Texto = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

class ProdutoEntrada(BaseModel):
    nome: Texto
    descricao: str = Field(default="", max_length=500)
    categoria: Texto
    preco_centavos: int = Field(ge=1, description="valor em centavos")
    ativo: bool = True
    tags: list[Texto] = Field(default_factory=list, max_length=15)
    
class ProdutoAtualizacao(BaseModel):
    nome: Texto | None = None
    descricao: str | None = Field(default=None, max_length=500)
    categoria: Texto | None = None
    preco_centavos: int | None = Field(default=None, ge=1)
    ativo: bool | None = None
    tags: list[Texto] | None = Field(default=None, max_length=15)
    
    @model_validator(mode="after")
    def nao_permitir_nulos(self):
        if any(value is None for value in self.model_dump(exclude_unset=True).values()):
            raise ValueError("Não envie campos nulos")
        return self
    
    
class ProdudoSaida(ProdutoEntrada):
    id: str
    
class ItemSolicitado(BaseModel):
    produto_id: str 
    quantidade: int = Field(ge=1, le=100)

class PedidoEntrada(BaseModel):
    cliente: Texto
    itens: list[ItemSolicitado] = Field(min_length=1, max_length=50)
    observacoes: str = Field(default="", max_length=500)
    
    @model_validator(mode="after")
    def itens_nao_repetidos(self):
        ids = [i.produto for i in self.itens]
        if len(ids) != len(set(ids)):
            raise ValueError("Informe cada produto uma única vez")
        return self
    
class ItemPedido(BaseModel):
    produto_id: str 
    nome: str 
    quantidade: int 
    preco_unitario_centavos: int
    subtotal_centavos: int 
    
class StatusPedido(str, Enum):
    pendente = "pendente"
    preparando = "preparando"
    pronto = "pronto"
    entregue = "entregue"
    cancelado = "cancelado"
    
class StatusAtualizacao(BaseModel):
    status: StatusPedido
    
    
class PedidoSaida(BaseModel):
    id: str
    cliente: str
    itens: list[ItemPedido]
    observacoes: str 
    status: StatusPedido
    total_centavos: int
    criado_em: datetime
    atualizado_em: datetime
    
class Mensagem(BaseModel):
    mensagem: str
    
class FaturamentoProduto(BaseModel):
    produto_id: str 
    nome: str 
    quantidade: int  
    faturamento_centavos: int
    
class ResumoPedido(BaseModel):
    total_pedidos: int
    total_faturamento_centavos: int
    por_status: dict[str, int] 
    