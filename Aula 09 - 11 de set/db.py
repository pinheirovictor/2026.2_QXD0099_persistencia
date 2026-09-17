import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """
    Abre uma conexão com o PostgreSQL.

    Esta função representa o objeto Connection da DB-API.
    Os valores podem ser alterados por variáveis de ambiente.
    """
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "astronomia"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "2023"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


def get_cursor(connection):
    """
    Cria um cursor DB-API.

    RealDictCursor faz o resultado vir como dicionário:
    {"id_clube": 1, "nome": "Clube Sirius"}
    """
    return connection.cursor(cursor_factory=RealDictCursor)
