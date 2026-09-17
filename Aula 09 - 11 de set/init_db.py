from pathlib import Path
from db import get_connection


def criar_tabelas():
    # Lemos todo o arquivo SQL.
    sql = Path("schema.sql").read_text(encoding="utf-8")

    # O bloco with confirma a transação automaticamente se tudo der certo.
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas()
