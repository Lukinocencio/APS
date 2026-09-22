# database/models.py

"""
Modelos de dados do sistema de reconhecimento facial usando SQLAlchemy ORM.
Define as tabelas Usuario e Documento.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    """
    Modelo da tabela de usuários do sistema.
    """
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    nivel_acesso = Column(String, nullable=False)

    def __repr__(self):
        """
        Retorna representação legível do usuário para debug.
        """
        return f"<Usuario(id={self.id}, nome='{self.nome}', nivel='{self.nivel_acesso}')>"

class Documento(Base):
    """
    Modelo da tabela de documentos do sistema.
    """
    __tablename__ = 'documentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False, unique=True)
    nome_arquivo_original = Column(String, nullable=False)
    tipo_arquivo = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)
    data_modificacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    nivel_permissao = Column(String, nullable=False, default='Nível C')

    def __repr__(self):
        """
        Retorna representação legível do documento para debug.
        """
        return f"<Documento(id={self.id}, titulo='{self.titulo}', caminho='{self.caminho_arquivo}')>"