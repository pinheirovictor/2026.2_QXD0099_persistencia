"""Importa os 5 conjuntos CE do TSE em lotes, sem Docker nem extrações no disco.

Exemplo: python -m scripts.importar_dados --uf CE
         python -m scripts.importar_dados --colecao bens --limite 50
"""
import argparse
import csv
import logging
import zipfile
from contextlib import ExitStack
from io import TextIOWrapper
from pathlib import Path

from pymongo import ReplaceOne
from pymongo.database import Database

from app.database import criar_indices, get_db
from scripts.tse_transformacao import ARQUIVOS, COLUNAS, TRANSFORMAR, campo

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("importar_tse")
PASTA_DADOS = Path(__file__).resolve().parents[1] / "dados"


def localizar_arquivo(pasta: Path, colecao: str, uf: str) -> Path:
    prefixo = ARQUIVOS[colecao]
    for nome in (f"{prefixo}_{uf}.zip", f"{prefixo}.zip", f"{prefixo}_{uf}.csv"):
        arquivo = pasta / nome
        if arquivo.is_file():
            return arquivo
    raise FileNotFoundError(
        f"Arquivo de {colecao} não encontrado em {pasta}. "
        f"Use {prefixo}_{uf}.zip (incluído) ou {prefixo}.zip (original do TSE)."
    )


def escolher_csv(nomes: list[str], prefixo: str, uf: str) -> str:
    arquivos = [n for n in nomes if n.lower().endswith('.csv')]
    for sufixo in (f"_{uf}.csv", "_BRASIL.csv"):
        candidatos = [n for n in arquivos if Path(n).name.lower().startswith(prefixo.lower())
                      and Path(n).name.upper().endswith(sufixo.upper())]
        if candidatos:
            return sorted(candidatos)[0]
    raise ValueError(f"Não existe CSV de {uf} nem BRASIL no ZIP de {prefixo}")


def importar_colecao(
    db: Database,
    colecao: str,
    arquivo: Path,
    uf: str = "CE",
    limite: int = 0,
    tamanho_lote: int = 1000,
) -> dict:
    if colecao not in TRANSFORMAR:
        raise ValueError(f"Coleção não suportada: {colecao}")
    uf = uf.upper()
    if len(uf) != 2 or not uf.isalpha():
        raise ValueError("UF inválida")
    if limite < 0 or tamanho_lote < 1:
        raise ValueError("Limite deve ser >= 0; lote deve ser >= 1")

    with ExitStack() as stack:
        if zipfile.is_zipfile(arquivo):
            z = stack.enter_context(zipfile.ZipFile(arquivo))
            nome_csv = escolher_csv(z.namelist(), ARQUIVOS[colecao], uf)
            binario = stack.enter_context(z.open(nome_csv))
        elif arquivo.suffix.lower() == '.csv':
            nome_csv = arquivo.name
            binario = stack.enter_context(arquivo.open('rb'))
        else:
            raise ValueError("Informe CSV ou ZIP")
        texto = stack.enter_context(TextIOWrapper(binario, encoding='latin-1', newline=''))
        leitor = csv.DictReader(texto, delimiter=';')
        faltando = COLUNAS[colecao] - set(leitor.fieldnames or [])
        if faltando:
            raise ValueError(f"Colunas ausentes em {nome_csv}: {', '.join(sorted(faltando))}")
        ops, total, ignorados = [], 0, 0
        for linha in leitor:
            if (campo(linha, 'SG_UF') or '').upper() != uf:
                continue
            try:
                registro = TRANSFORMAR[colecao](linha)
            except ValueError:
                ignorados += 1
                continue
            ops.append(ReplaceOne({'_id': registro['_id']}, registro, upsert=True))
            total += 1
            if len(ops) >= tamanho_lote:
                db[colecao].bulk_write(ops, ordered=False)
                ops.clear()
            if limite and total >= limite:
                break
        if ops:
            db[colecao].bulk_write(ops, ordered=False)

    logger.info("%s: %d registros processados, %d linhas ignoradas (%s)", colecao, total, ignorados, uf)
    return {'colecao': colecao, 'registros_processados': total, 'linhas_ignoradas': ignorados, 'uf': uf, 'csv': nome_csv}


def main() -> None:
    p = argparse.ArgumentParser(description='Importar CSV/ZIP do TSE para MongoDB local/Atlas')
    p.add_argument('--pasta', type=Path, default=PASTA_DADOS)
    p.add_argument('--uf', default='CE')
    p.add_argument('--colecao', choices=['todas', *ARQUIVOS], default='todas')
    p.add_argument('--limite', type=int, default=0, help='0 importa tudo')
    p.add_argument('--lote', type=int, default=1000)
    args = p.parse_args()
    escolhidas = list(ARQUIVOS) if args.colecao == 'todas' else [args.colecao]
    db = get_db()
    db.client.admin.command('ping')  # erro explícito se o servidor MongoDB não estiver ligado
    for nome in escolhidas:
        arquivo = localizar_arquivo(args.pasta, nome, args.uf.upper())
        resultado = importar_colecao(db, nome, arquivo, uf=args.uf, limite=args.limite, tamanho_lote=args.lote)
        print(resultado)
    criar_indices(db)
    print('Importação finalizada. Índices criados nas 5 coleções.')

if __name__ == '__main__':
    main()
