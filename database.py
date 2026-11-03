import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "faculends.db")

MATERIAIS_EXEMPLO = [
    ("Notebook Dell", "Notebook para aulas e projetos", "Informática", 5, 5),
    ("Projetor Epson", "Projetor multimídia para apresentações", "Audiovisual", 3, 3),
    ("Câmera Canon", "Câmera DSLR para gravação de trabalhos", "Audiovisual", 2, 2),
    ("Arduino Uno", "Kit de eletrônica para práticas de laboratório", "Eletrônica", 10, 10),
    ("Multímetro", "Medidor de tensão, corrente e resistência", "Eletrônica", 6, 6),
    ("Microfone de lapela", "Microfone sem fio para gravações", "Audiovisual", 4, 4),
    ("Tablet Samsung", "Tablet para atividades em sala", "Informática", 8, 8),
    ("Extensão elétrica", "Extensão de 5 metros com 4 tomadas", "Acessórios", 12, 12),
]


def get_db():
    """Abre a conexão com o banco. Outras partes do sistema usam esta função."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas (se não existirem) e insere os dados de exemplo."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT NOT NULL,
            quantidade_total INTEGER NOT NULL,
            quantidade_disponivel INTEGER NOT NULL
        )
        """
    )
    total = conn.execute("SELECT COUNT(*) FROM materiais").fetchone()[0]
    if total == 0:
        conn.executemany(
            """
            INSERT INTO materiais
            (nome, descricao, categoria, quantidade_total, quantidade_disponivel)
            VALUES (?, ?, ?, ?, ?)
            """,
            MATERIAIS_EXEMPLO,
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    conn = get_db()
    for m in conn.execute("SELECT * FROM materiais"):
        print(m["id"], m["nome"], "-", m["categoria"], "-", m["quantidade_disponivel"], "disponiveis")
    conn.close()