import sqlite3

conexao = sqlite3.connect("pontos.db")
conexao.execute("PRAGMA foreign_keys = ON")

# Tabela principal: os pontos marcados no mapa
conexao.execute("""
    CREATE TABLE IF NOT EXISTS pontos (
        id TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,              -- lixeira | descarte_irregular | bueiro_entupido
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        status TEXT NOT NULL,            -- pendente | validado | invalidado
        descricao TEXT,
        reportado_por TEXT,
        criado_em TEXT NOT NULL,
        atualizado_em TEXT NOT NULL,
        expira_em TEXT NOT NULL          -- 24h após a criação
    )
""")

# Fotos tiradas pelo usuário para aquele ponto (um ponto pode ter várias)
conexao.execute("""
    CREATE TABLE IF NOT EXISTS fotos (
        id TEXT PRIMARY KEY,
        ponto_id TEXT NOT NULL,
        caminho_arquivo TEXT NOT NULL,
        criado_em TEXT NOT NULL,
        FOREIGN KEY (ponto_id) REFERENCES pontos (id)
    )
""")

# Votos de validação (verdadeiro/falso) enquanto o ponto está pendente
conexao.execute("""
    CREATE TABLE IF NOT EXISTS votos (
        id TEXT PRIMARY KEY,
        ponto_id TEXT NOT NULL,
        voto TEXT NOT NULL,              -- verdadeiro | falso
        criado_em TEXT NOT NULL,
        FOREIGN KEY (ponto_id) REFERENCES pontos (id)
    )
""")

conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso! Tabelas: pontos, fotos, votos")