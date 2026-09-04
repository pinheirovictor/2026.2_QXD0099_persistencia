import json
from pathlib import Path
from typing import Any

from core.logging_config import logger


def garantir_arquivo(arquivo: Path) -> None:
    """Cria o arquivo JSON com uma lista vazia caso não exista."""
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    if not arquivo.exists():
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        logger.info("Arquivo JSON criado: %s", arquivo.name)


def ler_json(arquivo: Path) -> list[dict[str, Any]]:
    """Desserializa o arquivo JSON para uma lista Python."""
    garantir_arquivo(arquivo)

    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as erro:
        logger.error(
            "JSON inválido em %s: %s",
            arquivo.name,
            erro,
        )

        raise ValueError(
            f"O arquivo {arquivo.name} contém JSON inválido."
        ) from erro


def escrever_json(
    arquivo: Path,
    dados: list[dict[str, Any]],
) -> None:
    """Serializa dados Python e grava no arquivo JSON."""
    garantir_arquivo(arquivo)

    with open(arquivo, "w", encoding="utf-8") as file:
        json.dump(
            dados,
            file,
            ensure_ascii=False,
            indent=4,
        )

    logger.debug(
        "Arquivo %s atualizado com %d registro(s).",
        arquivo.name,
        len(dados),
    )


def buscar_por_id(
    arquivo: Path,
    registro_id: int,
) -> dict[str, Any] | None:
    dados = ler_json(arquivo)

    for item in dados:
        if item["id"] == registro_id:
            return item

    return None


def adicionar(
    arquivo: Path,
    novo_registro: dict[str, Any],
) -> None:
    dados = ler_json(arquivo)
    dados.append(novo_registro)
    escrever_json(arquivo, dados)


def atualizar(
    arquivo: Path,
    registro_id: int,
    novo_registro: dict[str, Any],
) -> bool:
    dados = ler_json(arquivo)

    for indice, item in enumerate(dados):
        if item["id"] == registro_id:
            novo_registro["id"] = registro_id
            dados[indice] = novo_registro

            escrever_json(
                arquivo,
                dados,
            )

            return True

    return False


def remover(
    arquivo: Path,
    registro_id: int,
) -> bool:
    dados = ler_json(arquivo)

    nova_lista = [
        item
        for item in dados
        if item["id"] != registro_id
    ]

    if len(nova_lista) == len(dados):
        return False

    escrever_json(
        arquivo,
        nova_lista,
    )

    return True
