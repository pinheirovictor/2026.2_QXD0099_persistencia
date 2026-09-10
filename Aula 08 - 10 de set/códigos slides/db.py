import psycopg2


# ---------------------------------------------------------
# FUNÇÃO DE CONEXÃO
# ---------------------------------------------------------

def get_connection():
    """
    Cria e retorna uma conexão com o PostgreSQL.

    A conexão representa o objeto Connection da DB-API.
    """

    conexao = psycopg2.connect(
        dbname="exemplo",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    return conexao


# ---------------------------------------------------------
# CRIAÇÃO DAS TABELAS
# ---------------------------------------------------------

def criar_tabelas():
    """
    Cria as tabelas utilizadas pela aplicação.

    O banco 'exemplo' deve existir previamente.
    """

    conexao = get_connection()
    cursor = conexao.cursor()

    try:

        # Tabela Usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)

        # Tabela Pedido
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedido (
                id SERIAL PRIMARY KEY,
                usuario_id INT REFERENCES usuario(id),
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) NOT NULL
            );
        """)

        # Tabela Produto
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                preco DECIMAL(10, 2) NOT NULL
            );
        """)

        # Tabela associativa PedidoProduto
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedido_produto (
                pedido_id INT REFERENCES pedido(id),
                produto_id INT REFERENCES produto(id),
                quantidade INT NOT NULL,

                PRIMARY KEY (
                    pedido_id,
                    produto_id
                )
            );
        """)

        # Confirma as alterações.
        conexao.commit()

        print("Tabelas criadas com sucesso.")

    except Exception as erro:

        # Caso alguma operação falhe,
        # desfaz as alterações da transação.
        conexao.rollback()

        print(
            "Erro ao criar tabelas:",
            erro
        )

    finally:

        # Fecha cursor e conexão.
        cursor.close()
        conexao.close()