from db import get_connection, get_cursor


# ============================================================
# CRUD DE CLUBE DE ASTRONOMIA
# ============================================================

def criar_clube(dados):
    """
    CREATE -> INSERT INTO.

    O %s é o placeholder usado pelo psycopg2.
    Os valores ficam separados da instrução SQL.
    """
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
    """READ -> SELECT de todos os clubes."""
    sql = """
        SELECT *
        FROM ClubeAstronomia
        ORDER BY id_clube;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def buscar_clube(id_clube):
    """READ -> SELECT filtrando pela chave primária."""
    sql = """
        SELECT *
        FROM ClubeAstronomia
        WHERE id_clube = %s;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, (id_clube,))
            return cursor.fetchone()


def atualizar_clube(id_clube, dados):
    """UPDATE -> altera um clube existente."""
    sql = """
        UPDATE ClubeAstronomia
        SET nome = %s,
            cidade = %s,
            fundacao = %s
        WHERE id_clube = %s
        RETURNING *;
    """

    parametros = (
        dados.nome,
        dados.cidade,
        dados.fundacao,
        id_clube,
    )

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()


def excluir_clube(id_clube):
    """DELETE -> remove um clube pela chave primária."""
    sql = """
        DELETE FROM ClubeAstronomia
        WHERE id_clube = %s
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, (id_clube,))
            return cursor.fetchone()


# ============================================================
# CRUD DE MEMBRO
# ============================================================

def criar_membro(dados):
    """
    CREATE de membro.

    id_clube é uma chave estrangeira.
    O PostgreSQL garante que o clube informado exista.
    """
    sql = """
        INSERT INTO Membro
            (id_membro, nome, email, id_clube)
        VALUES
            (%s, %s, %s, %s)
        RETURNING *;
    """

    parametros = (
        dados.id_membro,
        dados.nome,
        dados.email,
        dados.id_clube,
    )

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()


def listar_membros():
    """
    READ com LEFT JOIN.

    Além dos dados do membro, retornamos o nome do clube.
    """
    sql = """
        SELECT
            m.id_membro,
            m.nome,
            m.email,
            m.id_clube,
            c.nome AS nome_clube
        FROM Membro m
        LEFT JOIN ClubeAstronomia c
            ON c.id_clube = m.id_clube
        ORDER BY m.id_membro;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def buscar_membro(id_membro):
    sql = """
        SELECT
            m.id_membro,
            m.nome,
            m.email,
            m.id_clube,
            c.nome AS nome_clube
        FROM Membro m
        LEFT JOIN ClubeAstronomia c
            ON c.id_clube = m.id_clube
        WHERE m.id_membro = %s;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, (id_membro,))
            return cursor.fetchone()


def atualizar_membro(id_membro, dados):
    sql = """
        UPDATE Membro
        SET nome = %s,
            email = %s,
            id_clube = %s
        WHERE id_membro = %s
        RETURNING *;
    """

    parametros = (
        dados.nome,
        dados.email,
        dados.id_clube,
        id_membro,
    )

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()


def excluir_membro(id_membro):
    sql = """
        DELETE FROM Membro
        WHERE id_membro = %s
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, (id_membro,))
            return cursor.fetchone()


# ============================================================
# CADASTROS DAS DEMAIS TABELAS
# ============================================================

def criar_corpo(dados):
    sql = """
        INSERT INTO CorpoCeleste
            (id_corpo, nome, tipo, constelacao)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                sql,
                (
                    dados.id_corpo,
                    dados.nome,
                    dados.tipo,
                    dados.constelacao,
                ),
            )
            return cursor.fetchone()


def listar_corpos():
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                "SELECT * FROM CorpoCeleste ORDER BY id_corpo;"
            )
            return cursor.fetchall()


def criar_equipamento(dados):
    sql = """
        INSERT INTO Equipamento
            (id_equipamento, modelo, tipo, fabricante)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                sql,
                (
                    dados.id_equipamento,
                    dados.modelo,
                    dados.tipo,
                    dados.fabricante,
                ),
            )
            return cursor.fetchone()


def listar_equipamentos():
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                "SELECT * FROM Equipamento ORDER BY id_equipamento;"
            )
            return cursor.fetchall()


def criar_local(dados):
    sql = """
        INSERT INTO LocalObservacao
            (id_local, nome, latitude, longitude, altitude_m)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                sql,
                (
                    dados.id_local,
                    dados.nome,
                    dados.latitude,
                    dados.longitude,
                    dados.altitude_m,
                ),
            )
            return cursor.fetchone()


def listar_locais():
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                "SELECT * FROM LocalObservacao ORDER BY id_local;"
            )
            return cursor.fetchall()


def criar_evento(dados):
    sql = """
        INSERT INTO EventoObservacao
            (id_evento, titulo, data_evento, id_local)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                sql,
                (
                    dados.id_evento,
                    dados.titulo,
                    dados.data_evento,
                    dados.id_local,
                ),
            )
            return cursor.fetchone()


def listar_eventos():
    sql = """
        SELECT
            e.id_evento,
            e.titulo,
            e.data_evento,
            e.id_local,
            l.nome AS nome_local
        FROM EventoObservacao e
        LEFT JOIN LocalObservacao l
            ON l.id_local = e.id_local
        ORDER BY e.id_evento;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def organizar_evento(dados):
    """
    Insere na tabela associativa N:M.
    """
    sql = """
        INSERT INTO OrganizacaoEvento
            (id_evento, id_clube)
        VALUES (%s, %s)
        RETURNING *;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(
                sql,
                (
                    dados.id_evento,
                    dados.id_clube,
                ),
            )
            return cursor.fetchone()


def listar_clubes_do_evento(id_evento):
    """
    Exemplo de JOIN usando a tabela associativa.
    """
    sql = """
        SELECT
            e.id_evento,
            e.titulo AS evento,
            c.id_clube,
            c.nome AS clube
        FROM OrganizacaoEvento oe
        INNER JOIN EventoObservacao e
            ON e.id_evento = oe.id_evento
        INNER JOIN ClubeAstronomia c
            ON c.id_clube = oe.id_clube
        WHERE oe.id_evento = %s
        ORDER BY c.nome;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, (id_evento,))
            return cursor.fetchall()


def criar_observacao(dados):
    sql = """
        INSERT INTO Observacao (
            id_obs,
            id_membro,
            id_evento,
            id_corpo,
            id_equipamento,
            horario,
            condicoes_climaticas,
            anotacoes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """

    parametros = (
        dados.id_obs,
        dados.id_membro,
        dados.id_evento,
        dados.id_corpo,
        dados.id_equipamento,
        dados.horario,
        dados.condicoes_climaticas,
        dados.anotacoes,
    )

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()


def listar_observacoes():
    """
    Consulta final usando vários INNER JOINs.
    """
    sql = """
        SELECT
            o.id_obs,
            o.horario,
            o.condicoes_climaticas,
            o.anotacoes,

            m.nome AS membro,
            e.titulo AS evento,
            c.nome AS corpo_celeste,
            c.tipo AS tipo_corpo,
            eq.modelo AS equipamento

        FROM Observacao o

        INNER JOIN Membro m
            ON m.id_membro = o.id_membro

        INNER JOIN EventoObservacao e
            ON e.id_evento = o.id_evento

        INNER JOIN CorpoCeleste c
            ON c.id_corpo = o.id_corpo

        INNER JOIN Equipamento eq
            ON eq.id_equipamento = o.id_equipamento

        ORDER BY o.horario;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def estatisticas_por_tipo_corpo():
    """
    Exemplo de função agregada COUNT + GROUP BY.
    """
    sql = """
        SELECT
            c.tipo,
            COUNT(*) AS total_observacoes
        FROM Observacao o
        INNER JOIN CorpoCeleste c
            ON c.id_corpo = o.id_corpo
        GROUP BY c.tipo
        ORDER BY total_observacoes DESC;
    """

    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
