from db import get_connection, get_cursor


def criar_clube(dados):
    sql = """
        INSERT INTO ClubeAstronomia
            (id_clube, nome, cidade, fundacao)
        VALUES
            (%s, %s, %s, %s)
        RETURNING *;
    """
    
    parametros = (
        dados.id_clube,
        dados.nome,
        dados.cidade, 
        dados.fundacao,
    )
    
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()
    
def listar_clubes():
    sql = """
        SELECT *
        FROM ClubeAstronomia
        ORDER BY id_clube
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()