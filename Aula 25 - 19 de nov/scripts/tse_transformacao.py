"""Transformação dos 5 layouts reais de CSV do TSE 2024.

Sem dependências externas. Não importa CPF, título eleitoral, e-mail, data
pessoal de nascimento ou CNPJ de candidatura, mesmo que existam no CSV.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

AUSENTES = {"", "#NULO", "#NULO#", "#NE", "#NE#", "NULO", "NULL", "NÃO DIVULGÁVEL"}

COLUNAS = {
    "candidatos": {"ANO_ELEICAO", "CD_ELEICAO", "NR_TURNO", "SG_UF", "SG_UE", "CD_CARGO", "SQ_CANDIDATO", "SQ_COLIGACAO", "NM_CANDIDATO", "DS_CARGO", "SG_PARTIDO"},
    "bens": {"ANO_ELEICAO", "CD_ELEICAO", "SG_UF", "SQ_CANDIDATO", "NR_ORDEM_BEM_CANDIDATO", "VR_BEM_CANDIDATO"},
    "coligacoes": {"ANO_ELEICAO", "CD_ELEICAO", "NR_TURNO", "SG_UF", "SG_UE", "CD_CARGO", "SQ_COLIGACAO", "NR_PARTIDO"},
    "vagas": {"ANO_ELEICAO", "CD_ELEICAO", "SG_UF", "SG_UE", "CD_CARGO", "QT_VAGA"},
    "redes_sociais": {"AA_ELEICAO", "CD_ELEICAO", "SG_UF", "SQ_CANDIDATO", "NR_ORDEM_REDE_SOCIAL", "DS_URL"},
}

ARQUIVOS = {
    "candidatos": "consulta_cand_2024",
    "bens": "bem_candidato_2024",
    "coligacoes": "consulta_coligacao_2024",
    "vagas": "consulta_vagas_2024",
    "redes_sociais": "rede_social_candidato_2024",
}


def campo(linha: dict, chave: str) -> str | None:
    v = str(linha.get(chave, "") or "").strip()
    return None if v.upper() in AUSENTES else v


def inteiro(valor: str | None) -> int | None:
    try:
        return int(valor) if valor is not None else None
    except (ValueError, TypeError):
        return None


def data_iso(valor: str | None) -> str | None:
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return None


def centavos(valor: str | None) -> int | None:
    if valor is None:
        return None
    try:
        return int(Decimal(valor.replace(".", "").replace(",", ".")) * 100)
    except (InvalidOperation, ValueError):
        return None


def chave_candidato(ano, eleicao, uf, sequencial) -> str | None:
    if not all((ano, eleicao, uf, sequencial)):
        return None
    return "_".join((ano, eleicao, uf, sequencial))


def chave_coligacao(ano, eleicao, uf, ue, coligacao) -> str | None:
    if not all((ano, eleicao, uf, ue, coligacao)):
        return None
    return "_".join((ano, eleicao, uf, ue, coligacao))


def chave_vaga(ano, eleicao, uf, ue, cargo) -> str | None:
    if not all((ano, eleicao, uf, ue, cargo)):
        return None
    return "_".join((ano, eleicao, uf, ue, cargo))


def identificador(*partes: str | None) -> str:
    if not all(partes):
        raise ValueError("Linha sem identificadores mínimos")
    return "tse_" + "_".join(partes)


def transformar_candidato(r: dict) -> dict:
    c = lambda k: campo(r, k)
    ano, eleicao, turno, uf = c("ANO_ELEICAO"), c("CD_ELEICAO"), c("NR_TURNO"), c("SG_UF")
    ue, cargo, sq = c("SG_UE"), c("CD_CARGO"), c("SQ_CANDIDATO")
    return {
        "_id": identificador(ano, eleicao, turno, uf, sq),
        "origem": "tse", "ano": inteiro(ano), "cd_eleicao": eleicao,
        "turno": inteiro(turno), "uf": uf, "sg_ue": ue,
        "municipio": c("NM_UE") or "NÃO INFORMADO",
        "cd_cargo": cargo, "cargo": c("DS_CARGO") or "NÃO INFORMADO",
        "sq_candidato": sq, "chave_candidato": chave_candidato(ano, eleicao, uf, sq),
        "sq_coligacao": c("SQ_COLIGACAO"),
        "chave_coligacao": chave_coligacao(ano, eleicao, uf, ue, c("SQ_COLIGACAO")),
        "chave_vaga": chave_vaga(ano, eleicao, uf, ue, cargo),
        "nome": c("NM_CANDIDATO") or "NÃO INFORMADO",
        "nome_urna": c("NM_URNA_CANDIDATO"), "numero": c("NR_CANDIDATO"),
        "partido": c("SG_PARTIDO") or "NÃO INFORMADO",
        "numero_partido": c("NR_PARTIDO"),
        "nome_partido": c("NM_PARTIDO"),
        "situacao": c("DS_SIT_TOT_TURNO"),
        "data_eleicao": data_iso(c("DT_ELEICAO")),
        "situacao_candidatura": c("DS_SITUACAO_CANDIDATURA"),
    }


def transformar_bem(r: dict) -> dict:
    c = lambda k: campo(r, k)
    ano, eleicao, uf, sq = c("ANO_ELEICAO"), c("CD_ELEICAO"), c("SG_UF"), c("SQ_CANDIDATO")
    ordem = c("NR_ORDEM_BEM_CANDIDATO")
    return {
        "_id": identificador(ano, eleicao, uf, sq, ordem),
        "origem": "tse", "ano": inteiro(ano), "cd_eleicao": eleicao,
        "uf": uf, "sg_ue": c("SG_UE"), "municipio": c("NM_UE"),
        "sq_candidato": sq, "chave_candidato": chave_candidato(ano, eleicao, uf, sq),
        "ordem": inteiro(ordem), "cd_tipo_bem": c("CD_TIPO_BEM_CANDIDATO"),
        "tipo_bem": c("DS_TIPO_BEM_CANDIDATO"),
        "descricao": c("DS_BEM_CANDIDATO"),
        "valor_centavos": centavos(c("VR_BEM_CANDIDATO")),
        "data_eleicao": data_iso(c("DT_ELEICAO")),
        "data_atualizacao": data_iso(c("DT_ULT_ATUAL_BEM_CANDIDATO")),
    }


def transformar_coligacao(r: dict) -> dict:
    c = lambda k: campo(r, k)
    ano, eleicao, turno, uf = c("ANO_ELEICAO"), c("CD_ELEICAO"), c("NR_TURNO"), c("SG_UF")
    ue, cargo, sq, nr = c("SG_UE"), c("CD_CARGO"), c("SQ_COLIGACAO"), c("NR_PARTIDO")
    return {
        # Inclui cargo e UE: um SQ_COLIGACAO pode aparecer em vários cargos/partidos.
        "_id": identificador(ano, eleicao, turno, uf, ue, cargo, sq, nr),
        "origem": "tse", "ano": inteiro(ano), "cd_eleicao": eleicao,
        "turno": inteiro(turno), "uf": uf, "sg_ue": ue,
        "municipio": c("NM_UE"), "cd_cargo": cargo,
        "cargo": c("DS_CARGO"), "sq_coligacao": sq,
        "chave_coligacao": chave_coligacao(ano, eleicao, uf, ue, sq),
        "partido": c("SG_PARTIDO"), "numero_partido": nr,
        "nome_partido": c("NM_PARTIDO"),
        "nome_coligacao": c("NM_COLIGACAO"),
        "composicao": c("DS_COMPOSICAO_COLIGACAO"),
        "tipo_agremiacao": c("TP_AGREMIACAO"),
        "situacao": c("DS_SITUACAO"),
        "data_eleicao": data_iso(c("DT_ELEICAO")),
    }


def transformar_vaga(r: dict) -> dict:
    c = lambda k: campo(r, k)
    ano, eleicao, uf, ue, cargo = c("ANO_ELEICAO"), c("CD_ELEICAO"), c("SG_UF"), c("SG_UE"), c("CD_CARGO")
    return {
        "_id": identificador(ano, eleicao, uf, ue, cargo),
        "origem": "tse", "ano": inteiro(ano), "cd_eleicao": eleicao,
        "uf": uf, "sg_ue": ue, "municipio": c("NM_UE"),
        "cd_cargo": cargo, "cargo": c("DS_CARGO"),
        "chave_vaga": chave_vaga(ano, eleicao, uf, ue, cargo),
        "quantidade": inteiro(c("QT_VAGA")),
        "data_eleicao": data_iso(c("DT_ELEICAO")),
        "data_posse": data_iso(c("DT_POSSE")),
    }


def transformar_rede_social(r: dict) -> dict:
    c = lambda k: campo(r, k)
    ano, eleicao, uf, sq = c("AA_ELEICAO"), c("CD_ELEICAO"), c("SG_UF"), c("SQ_CANDIDATO")
    ordem, url = c("NR_ORDEM_REDE_SOCIAL"), c("DS_URL")
    # Algumas entradas não são URLs válidas; nesse caso, domínio = None.
    parsed = urlparse(url or "")
    dominio = parsed.netloc.lower() if parsed.scheme in {"http", "https"} else None
    return {
        "_id": identificador(ano, eleicao, uf, sq, ordem),
        "origem": "tse", "ano": inteiro(ano), "cd_eleicao": eleicao,
        "uf": uf, "sq_candidato": sq,
        "chave_candidato": chave_candidato(ano, eleicao, uf, sq),
        "ordem": inteiro(ordem), "url": url,
        "dominio": dominio, "tipo_eleicao": c("NM_TIPO_ELEICAO"),
        "eleicao": c("DS_ELEICAO"),
    }

TRANSFORMAR = {
    "candidatos": transformar_candidato,
    "bens": transformar_bem,
    "coligacoes": transformar_coligacao,
    "vagas": transformar_vaga,
    "redes_sociais": transformar_rede_social,
}