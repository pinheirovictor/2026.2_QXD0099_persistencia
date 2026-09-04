from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from core.logging_config import logger
from models.livro import Livro
from services.json_repository import (
    adicionar,
    atualizar,
    buscar_por_id,
    ler_json,
    remover,
)


BASE_DIR = Path(__file__).resolve().parent.parent
LIVROS_FILE = BASE_DIR / "data" / "livros.json"

router = APIRouter(
    prefix="/livros",
    tags=["Livros"],
)


@router.post(
    "",
    response_model=Livro,
    status_code=status.HTTP_201_CREATED,
)
def criar_livro(livro: Livro):
    if buscar_por_id(
        LIVROS_FILE,
        livro.id,
    ):
        logger.warning(
            "Tentativa de cadastrar livro com ID duplicado: %s",
            livro.id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Livro com este ID já existe.",
        )

    dados = livro.model_dump(
        mode="json"
    )

    adicionar(
        LIVROS_FILE,
        dados,
    )

    logger.info(
        "Livro cadastrado: id=%s, titulo=%s",
        livro.id,
        livro.titulo,
    )

    return livro


@router.get(
    "",
    response_model=list[Livro],
)
def listar_livros():
    livros = ler_json(
        LIVROS_FILE
    )

    logger.info(
        "Listagem de livros: %d registro(s).",
        len(livros),
    )

    return livros


@router.get(
    "/{livro_id}",
    response_model=Livro,
)
def obter_livro(livro_id: int):
    livro = buscar_por_id(
        LIVROS_FILE,
        livro_id,
    )

    if not livro:
        logger.warning(
            "Livro não encontrado: %s",
            livro_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado.",
        )

    return livro


@router.put(
    "/{livro_id}",
    response_model=Livro,
)
def atualizar_livro(
    livro_id: int,
    livro: Livro,
):
    dados = livro.model_dump(
        mode="json"
    )

    dados["id"] = livro_id

    if not atualizar(
        LIVROS_FILE,
        livro_id,
        dados,
    ):
        logger.warning(
            "Tentativa de atualizar livro inexistente: %s",
            livro_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado.",
        )

    logger.info(
        "Livro atualizado: %s",
        livro_id,
    )

    return dados


@router.delete(
    "/{livro_id}",
    status_code=status.HTTP_200_OK,
)
def excluir_livro(livro_id: int):
    if not remover(
        LIVROS_FILE,
        livro_id,
    ):
        logger.warning(
            "Tentativa de remover livro inexistente: %s",
            livro_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado.",
        )

    logger.info(
        "Livro removido: %s",
        livro_id,
    )

    return {
        "mensagem": "Livro removido com sucesso."
    }
