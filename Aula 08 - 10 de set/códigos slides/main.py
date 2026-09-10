from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

import psycopg2

import crud

from db import criar_tabelas

from models import (
    UsuarioCreate,
    ProdutoCreate,
    PedidoCreate,
    PedidoProdutoCreate
)


# ---------------------------------------------------------
# APLICAÇÃO
# ---------------------------------------------------------

app = FastAPI(
    title="API de Pedidos",
    description=(
        "Exemplo de FastAPI + PostgreSQL "
        "utilizando DB-API sem ORM."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# CRIAÇÃO DAS TABELAS
# ---------------------------------------------------------

@app.on_event("startup")
def startup():

    criar_tabelas()


# =========================================================
# USUÁRIOS
# =========================================================


@app.post(
    "/usuarios",
    status_code=201
)
def criar_usuario(
    usuario: UsuarioCreate
):

    try:

        return crud.criar_usuario(
            usuario
        )

    except psycopg2.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail=(
                "E-mail já cadastrado."
            )
        )


@app.get("/usuarios")
def listar_usuarios():

    return crud.listar_usuarios()


@app.get(
    "/usuarios/{usuario_id}"
)
def buscar_usuario(
    usuario_id: int
):

    usuario = crud.buscar_usuario(
        usuario_id
    )

    if usuario is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario


@app.put(
    "/usuarios/{usuario_id}"
)
def atualizar_usuario(
    usuario_id: int,
    usuario: UsuarioCreate
):

    resultado = crud.atualizar_usuario(
        usuario_id,
        usuario
    )

    if resultado is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return resultado


@app.delete(
    "/usuarios/{usuario_id}"
)
def excluir_usuario(
    usuario_id: int
):

    try:

        resultado = crud.excluir_usuario(
            usuario_id
        )

    except psycopg2.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail=(
                "Usuário possui pedidos "
                "e não pode ser removido."
            )
        )

    if resultado is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "mensagem":
            "Usuário excluído.",

        "usuario":
            resultado
    }


# =========================================================
# PRODUTOS
# =========================================================


@app.post(
    "/produtos",
    status_code=201
)
def criar_produto(
    produto: ProdutoCreate
):

    return crud.criar_produto(
        produto
    )


@app.get("/produtos")
def listar_produtos():

    return crud.listar_produtos()


@app.get(
    "/produtos/{produto_id}"
)
def buscar_produto(
    produto_id: int
):

    produto = crud.buscar_produto(
        produto_id
    )

    if produto is None:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return produto


@app.put(
    "/produtos/{produto_id}"
)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoCreate
):

    resultado = crud.atualizar_produto(
        produto_id,
        produto
    )

    if resultado is None:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return resultado


@app.delete(
    "/produtos/{produto_id}"
)
def excluir_produto(
    produto_id: int
):

    try:

        resultado = crud.excluir_produto(
            produto_id
        )

    except psycopg2.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail=(
                "Produto está associado "
                "a um pedido."
            )
        )

    if resultado is None:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return {
        "mensagem":
            "Produto excluído.",

        "produto":
            resultado
    }


# =========================================================
# PEDIDOS
# =========================================================


@app.post(
    "/pedidos",
    status_code=201
)
def criar_pedido(
    pedido: PedidoCreate
):

    try:

        return crud.criar_pedido(
            pedido
        )

    except psycopg2.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail=(
                "Usuário informado "
                "não existe."
            )
        )


@app.get("/pedidos")
def listar_pedidos():

    return crud.listar_pedidos()


@app.get(
    "/pedidos/{pedido_id}"
)
def buscar_pedido(
    pedido_id: int
):

    pedido = crud.buscar_pedido(
        pedido_id
    )

    if pedido is None:

        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    return pedido


# =========================================================
# PEDIDO x PRODUTO
# =========================================================


@app.post(
    "/pedidos/produtos",
    status_code=201
)
def adicionar_produto_pedido(
    dados: PedidoProdutoCreate
):

    try:

        return crud.adicionar_produto_pedido(
            dados
        )

    except psycopg2.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail=(
                "Pedido/produto não existe "
                "ou associação já cadastrada."
            )
        )


@app.get(
    "/pedidos/{pedido_id}/produtos"
)
def listar_produtos_pedido(
    pedido_id: int
):

    return crud.listar_produtos_pedido(
        pedido_id
    )


# ---------------------------------------------------------
# ENDPOINT INICIAL
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "mensagem":
            "API funcionando",

        "documentacao":
            "/docs"
    }