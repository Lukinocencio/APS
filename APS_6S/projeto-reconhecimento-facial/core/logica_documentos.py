# core/logica_documentos.py

"""
Lógica de manipulação de documentos do sistema.
Inclui funções para criar, consultar, editar e deletar documentos.
"""

import os
import shutil
import uuid
from database.setup import SessionLocal
from database.models import Usuario, Documento

class LogicaDocumentos:
    """
    Classe responsável pela lógica de manipulação de documentos.
    """
    def __init__(self, diretorio_documentos="arquivos_gerenciados"):
        """
        Inicializa o gerenciador de documentos, criando diretório se necessário.
        """
        self.diretorio_documentos = diretorio_documentos
        if not os.path.exists(self.diretorio_documentos):
            os.makedirs(self.diretorio_documentos)

    def get_documentos_para_usuario(self, usuario: Usuario):
        """
        Retorna lista de documentos acessíveis conforme nível do usuário.
        """
        db = SessionLocal()
        try:
            niveis_permitidos = []
            if usuario.nivel_acesso == 'Ministro':
                niveis_permitidos = ['Ministro', 'Diretor', 'Servidor']
            elif usuario.nivel_acesso == 'Diretor':
                niveis_permitidos = ['Diretor', 'Servidor']
            elif usuario.nivel_acesso == 'Servidor':
                niveis_permitidos = ['Servidor']
            return db.query(Documento).filter(Documento.nivel_permissao.in_(niveis_permitidos)).all()
        finally:
            db.close()

    def criar_documento_de_arquivo(self, caminho_origem: str, titulo: str, nivel_permissao: str) -> Documento | None:
        """
        Copia um arquivo para a pasta gerenciada e salva seu caminho no banco.
        """
        if not os.path.exists(caminho_origem):
            print("Erro: Caminho de origem não existe.")
            return None

        db = SessionLocal()
        try:
            nome_original = os.path.basename(caminho_origem)
            tipo_arquivo = nome_original.split('.')[-1].lower()
            nome_unico = f"{uuid.uuid4()}.{tipo_arquivo}"
            caminho_destino = os.path.join(self.diretorio_documentos, nome_unico)
            shutil.copy(caminho_origem, caminho_destino)
            novo_documento = Documento(
                titulo=titulo,
                caminho_arquivo=caminho_destino,
                nome_arquivo_original=nome_original,
                tipo_arquivo=tipo_arquivo,
                nivel_permissao=nivel_permissao
            )
            db.add(novo_documento)
            db.commit()
            db.refresh(novo_documento)
            return novo_documento
        except Exception as e:
            print(f"Erro ao criar documento: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def atualizar_conteudo_texto(self, doc_id: int, novo_conteudo_texto: str) -> bool:
        """
        Atualiza o conteúdo de um documento de texto pelo id.
        """
        db = SessionLocal()
        try:
            documento = db.query(Documento).filter(Documento.id == doc_id).first()
            if documento and documento.tipo_arquivo == 'txt':
                with open(documento.caminho_arquivo, 'w', encoding='utf-8') as f:
                    f.write(novo_conteudo_texto)
                db.commit()
                return True
            return False
        finally:
            db.close()

    def deletar_documento(self, doc_id: int) -> bool:
        """
        Deleta o arquivo físico e o registro do banco de dados.
        """
        db = SessionLocal()
        try:
            documento = db.query(Documento).filter(Documento.id == doc_id).first()
            if documento:
                if os.path.exists(documento.caminho_arquivo):
                    os.remove(documento.caminho_arquivo)
                db.delete(documento)
                db.commit()
                return True
            return False
        finally:
            db.close()
            
