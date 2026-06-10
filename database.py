import sqlite3

DB_NAME = "financeiro.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha BLOB
    )
    """)

    # CORRIGIDO: adicionado usuario_id na tabela transacoes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria TEXT NOT NULL,
        tipo TEXT NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acao TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_log(acao):

    conn = get_connection()

    conn.execute(
        "INSERT INTO logs(acao) VALUES(?)",
        (acao,)
    )

    conn.commit()
    conn.close()

def add_user(usuario, senha):

    conn = get_connection()

    conn.execute(
        "INSERT INTO usuarios(usuario, senha) VALUES(?,?)",
        (usuario, senha)
    )

    conn.commit()
    conn.close()

def get_user(usuario):

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM usuarios WHERE usuario=?",
        (usuario,)
    ).fetchone()

    conn.close()

    return user

def add_transaction(usuario_id, descricao, valor, categoria, tipo):

    conn = get_connection()

    conn.execute("""
    INSERT INTO transacoes
    (usuario_id, descricao, valor, categoria, tipo)
    VALUES (?, ?, ?, ?, ?)
    """, (usuario_id, descricao, valor, categoria, tipo))

    conn.commit()
    conn.close()

def get_transactions(usuario_id):

    conn = get_connection()

    # CORRIGIDO: seleciona apenas as 6 colunas que o DataFrame espera
    dados = conn.execute("""
    SELECT id, descricao, valor, categoria, tipo, data
    FROM transacoes
    WHERE usuario_id=?
    ORDER BY data DESC
    """, (usuario_id,)).fetchall()

    conn.close()

    return dados

def delete_transaction(id_transacao):

    conn = get_connection()

    conn.execute(
        "DELETE FROM transacoes WHERE id=?",
        (id_transacao,)
    )

    conn.commit()
    conn.close()

def get_logs():

    conn = get_connection()

    logs = conn.execute("""
    SELECT *
    FROM logs
    ORDER BY data DESC
    """).fetchall()

    conn.close()

    return logs