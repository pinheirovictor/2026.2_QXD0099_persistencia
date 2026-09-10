from pydantic import BaseModel, Field


# ---------------------------------------------------------
# USUÁRIO
# ---------------------------------------------------------

class UsuarioCreate(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=100
    )

    email: str = Field(
        min_length=5,
        max_length=100
    )


# ---------------------------------------------------------
# PRODUTO
# ---------------------------------------------------------

class ProdutoCreate(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=100
    )

    preco: float = Field(
        gt=0
    )


# ---------------------------------------------------------
# PEDIDO
# ---------------------------------------------------------

class PedidoCreate(BaseModel):

    # FK para Usuario
    usuario_id: int = Field(
        gt=0
    )

    status: str = Field(
        min_length=2,
        max_length=20
    )


# ---------------------------------------------------------
# PEDIDO x PRODUTO
# ---------------------------------------------------------

class PedidoProdutoCreate(BaseModel):

    pedido_id: int = Field(
        gt=0
    )

    produto_id: int = Field(
        gt=0
    )

    quantidade: int = Field(
        gt=0
    )