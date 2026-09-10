from db import get_connection


# =========================================================
# USUÁRIO
# =========================================================


def criar_usuario(usuario):
    """
    CREATE

    Insere um usuário no banco.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        consulta = """
            INSERT INTO usuario (
                nome,
                email
            )
            VALUES (%s, %s)
            RETURNING id, nome, email;
        """

        parametros = (
            usuario.nome,
            usuario.email
        )

        cursor.execute(
            consulta,
            parametros
        )

        usuario_criado = cursor.fetchone()

        conexao.commit()

        return usuario_criado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def listar_usuarios():
    """
    READ

    Retorna todos os usuários.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                nome,
                email
            FROM usuario
            ORDER BY id;
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conexao.close()


def buscar_usuario(usuario_id):
    """
    READ

    Busca um usuário pela chave primária.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                nome,
                email
            FROM usuario
            WHERE id = %s;
            """,
            (usuario_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        conexao.close()


def atualizar_usuario(
    usuario_id,
    usuario
):
    """
    UPDATE
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE usuario

            SET
                nome = %s,
                email = %s

            WHERE id = %s

            RETURNING
                id,
                nome,
                email;
            """,
            (
                usuario.nome,
                usuario.email,
                usuario_id
            )
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def excluir_usuario(usuario_id):
    """
    DELETE
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM usuario

            WHERE id = %s

            RETURNING
                id,
                nome,
                email;
            """,
            (usuario_id,)
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


# =========================================================
# PRODUTO
# =========================================================


def criar_produto(produto):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO produto (
                nome,
                preco
            )

            VALUES (%s, %s)

            RETURNING
                id,
                nome,
                preco;
            """,
            (
                produto.nome,
                produto.preco
            )
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def listar_produtos():

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                nome,
                preco

            FROM produto

            ORDER BY id;
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conexao.close()


def buscar_produto(produto_id):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                nome,
                preco

            FROM produto

            WHERE id = %s;
            """,
            (produto_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        conexao.close()


def atualizar_produto(
    produto_id,
    produto
):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE produto

            SET
                nome = %s,
                preco = %s

            WHERE id = %s

            RETURNING
                id,
                nome,
                preco;
            """,
            (
                produto.nome,
                produto.preco,
                produto_id
            )
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def excluir_produto(produto_id):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM produto

            WHERE id = %s

            RETURNING
                id,
                nome,
                preco;
            """,
            (produto_id,)
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


# =========================================================
# PEDIDO
# =========================================================


def criar_pedido(pedido):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO pedido (
                usuario_id,
                status
            )

            VALUES (%s, %s)

            RETURNING
                id,
                usuario_id,
                data_pedido,
                status;
            """,
            (
                pedido.usuario_id,
                pedido.status
            )
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def listar_pedidos():
    """
    JOIN entre pedido e usuário.

    Em vez de mostrar somente usuario_id,
    também mostramos o nome do usuário.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                p.id,
                p.data_pedido,
                p.status,

                u.id AS usuario_id,
                u.nome AS usuario

            FROM pedido p

            INNER JOIN usuario u
                ON u.id = p.usuario_id

            ORDER BY p.id;
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conexao.close()


def buscar_pedido(pedido_id):

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            SELECT
                p.id,
                p.data_pedido,
                p.status,

                u.id AS usuario_id,
                u.nome AS usuario

            FROM pedido p

            INNER JOIN usuario u
                ON u.id = p.usuario_id

            WHERE p.id = %s;
            """,
            (pedido_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        conexao.close()


# =========================================================
# PEDIDO x PRODUTO
# =========================================================


def adicionar_produto_pedido(
    dados
):
    """
    CREATE na tabela associativa.

    Representa o relacionamento N:M.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO pedido_produto (
                pedido_id,
                produto_id,
                quantidade
            )

            VALUES (%s, %s, %s)

            RETURNING
                pedido_id,
                produto_id,
                quantidade;
            """,
            (
                dados.pedido_id,
                dados.produto_id,
                dados.quantidade
            )
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return resultado

    except Exception:

        conexao.rollback()
        raise

    finally:

        cursor.close()
        conexao.close()


def listar_produtos_pedido(
    pedido_id
):
    """
    JOIN entre:

    PedidoProduto
        +
    Produto
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            SELECT
                pp.pedido_id,

                p.id AS produto_id,
                p.nome AS produto,
                p.preco,

                pp.quantidade,

                p.preco * pp.quantidade
                    AS subtotal

            FROM pedido_produto pp

            INNER JOIN produto p
                ON p.id = pp.produto_id

            WHERE pp.pedido_id = %s;
            """,
            (pedido_id,)
        )

        return cursor.fetchall()

    finally:

        cursor.close()
        conexao.close()