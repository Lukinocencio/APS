# database/setup.py

"""
Configuração do banco de dados SQLite usando SQLAlchemy.
Define engine, sessão e inicialização das tabelas do sistema.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DB_PATH = "sqlite:///assets/banco.db"
engine = create_engine(DB_PATH, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Inicializa o banco de dados, criando todas as tabelas definidas em models.py.
    Executa apenas se as tabelas ainda não existirem.
    """
    print("Inicializando o banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados pronto.")