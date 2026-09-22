# interface/main_screen.py

"""
Tela principal do sistema de reconhecimento facial.
Permite visualizar, criar, editar e deletar documentos conforme permissões do usuário.
Gerencia interface, eventos e integração com lógica de documentos.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import fitz
import docx

class CriarDocumentoDialog(ctk.CTkToplevel):
    """
    Diálogo para criação de novo documento, recebendo lista de níveis de permissão.
    """
    def __init__(self, parent, niveis_disponiveis):
        super().__init__(parent)
        self.title("Novo Documento")
        self.geometry("400x200")
        self.transient(parent)
        self.grab_set()
        self.resultado = None
        ctk.CTkLabel(self, text="Título do Documento:").pack(padx=20, pady=(10, 0))
        self.titulo_entry = ctk.CTkEntry(self, width=360)
        self.titulo_entry.pack(padx=20, pady=5)
        ctk.CTkLabel(self, text="Nível de Permissão:").pack(padx=20, pady=(10, 0))
        self.nivel_combo = ctk.CTkOptionMenu(self, values=niveis_disponiveis, width=360)
        self.nivel_combo.pack(padx=20, pady=5)
        if niveis_disponiveis:
            self.nivel_combo.set(niveis_disponiveis[0])
        ok_button = ctk.CTkButton(self, text="Criar", command=self._on_ok)
        ok_button.pack(side="left", expand=True, padx=20, pady=10)
        cancel_button = ctk.CTkButton(self, text="Cancelar", command=self.destroy, fg_color="gray50")
        cancel_button.pack(side="right", expand=True, padx=20, pady=10)

    def _on_ok(self):
        """
        Valida e retorna os dados do novo documento.
        """
        titulo = self.titulo_entry.get()
        if not titulo:
            messagebox.showwarning("Atenção", "O título é obrigatório.", parent=self)
            return
        self.resultado = {"titulo": titulo, "nivel_permissao": self.nivel_combo.get()}
        self.destroy()

    def get_input(self):
        """
        Espera o fechamento do diálogo e retorna os dados inseridos.
        """
        self.wait_window()
        return self.resultado

class MainScreen:
    """
    Tela principal para manipulação de documentos conforme permissões do usuário.
    """
    def __init__(self, root, doc_logic, user, on_logout):
        """
        Inicializa a tela principal, widgets e configurações de layout.
        Args:
            root: Janela principal do Tkinter.
            doc_logic: Lógica de documentos.
            user: Usuário autenticado.
            on_logout: Função chamada ao realizar logout.
        """
        self.root = root
        self.doc_logic = doc_logic
        self.current_user = user
        self.on_logout = on_logout
        self.documento_selecionado = None
        self.root.title(f"Visualizador de Documentos | Nível: {self.current_user.nivel_acesso}")
        self.container = ctk.CTkFrame(root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        left_frame = ctk.CTkFrame(self.container)
        left_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ns")
        ctk.CTkLabel(left_frame, text="Documentos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        self.lista_docs_frame = ctk.CTkScrollableFrame(left_frame, label_text="")
        self.lista_docs_frame.pack(fill="y", expand=True, padx=5, pady=5)
        self.right_frame = ctk.CTkFrame(self.container)
        self.right_frame.grid(row=0, column=1, padx=0, pady=5, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.textbox = ctk.CTkTextbox(self.right_frame, font=("Consolas", 14))
        self.image_label = ctk.CTkLabel(self.right_frame, text="")
        self.unsupported_label = ctk.CTkLabel(self.right_frame, text="Selecione um documento para visualizar.", font=ctk.CTkFont(size=16))
        self.unsupported_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.carregar_lista_de_documentos()
        self.configurar_botoes_e_permissoes()
        ctk.CTkButton(left_frame, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=5, pady=10)

    def criar_novo_documento(self):
        """
        Abre seletor de arquivos e diálogo para criar novo documento, respeitando permissões do usuário.
        """
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo para salvar no sistema",
            filetypes=[("Todos os arquivos", "*.*"), ("PDF", "*.pdf"), ("Texto", "*.txt")]
        )
        if not caminho_arquivo:
            return

        niveis_disponiveis = []
        nivel_usuario = self.current_user.nivel_acesso
        if nivel_usuario == 'Ministro':
            niveis_disponiveis = ['Ministro', 'Diretor', 'Servidor']
        elif nivel_usuario == 'Diretor':
            niveis_disponiveis = ['Diretor', 'Servidor']
        elif nivel_usuario == 'Servidor':
            niveis_disponiveis = ['Servidor']

        dialog = CriarDocumentoDialog(self.root, niveis_disponiveis)
        dados = dialog.get_input()

        if dados:
            doc_criado = self.doc_logic.criar_documento_de_arquivo(
                caminho_origem=caminho_arquivo,
                titulo=dados['titulo'],
                nivel_permissao=dados['nivel_permissao']
            )
            if doc_criado:
                self.carregar_lista_de_documentos()
            else:
                messagebox.showerror("Erro", "Falha ao salvar o documento no banco de dados.")


    def selecionar_documento(self, documento):
        """
        Seleciona e exibe o documento escolhido, conforme tipo e permissões.
        """
        self.documento_selecionado = documento
        caminho_arquivo = documento.caminho_arquivo
        ext = documento.tipo_arquivo
        self.textbox.configure(state="normal")
        if not os.path.exists(caminho_arquivo):
            self._mostrar_visualizador('nao_suportado')
            self.unsupported_label.configure(text=f"ERRO: Arquivo não encontrado.")
            return
        if ext == 'txt':
            self._mostrar_visualizador('texto')
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                self.textbox.delete("1.0", "end")
                self.textbox.insert("1.0", f.read())
        elif ext == 'docx':
            self._mostrar_visualizador('texto')
            self._visualizar_docx(caminho_arquivo)
        elif ext == 'pdf':
            self._mostrar_visualizador('imagem')
            self._visualizar_pdf(caminho_arquivo)
        elif ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
            self._mostrar_visualizador('imagem')
            self._visualizar_imagem(caminho_arquivo)
        else:
            self._mostrar_visualizador('nao_suportado')
            self.unsupported_label.configure(text=f"Formato '.{ext}' não suportado.")
        if self.current_user.nivel_acesso == 'Servidor' and ext == 'txt':
            self.textbox.configure(state="disabled")


    def salvar_documento_atual(self):
        """
        Salva alterações no documento de texto selecionado.
        """
        if not self.documento_selecionado or self.documento_selecionado.tipo_arquivo != 'txt':
            messagebox.showwarning("Atenção", "Apenas documentos de texto (.txt) podem ser editados.")
            return
        conteudo_texto = self.textbox.get("1.0", "end-1c")
        if self.doc_logic.atualizar_conteudo_texto(self.documento_selecionado.id, conteudo_texto):
            messagebox.showinfo("Sucesso", "Documento salvo!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao salvar.")

            
    def carregar_lista_de_documentos(self):
        """
        Carrega e exibe a lista de documentos disponíveis para o usuário.
        """
        for widget in self.lista_docs_frame.winfo_children():
            widget.destroy()
        documentos = self.doc_logic.get_documentos_para_usuario(self.current_user)
        for doc in documentos:
            btn_text = f"{doc.titulo} ({doc.nome_arquivo_original})"
            ctk.CTkButton(self.lista_docs_frame, text=btn_text, command=lambda d=doc: self.selecionar_documento(d), anchor="w").pack(fill="x", pady=2)

            
    def deletar_documento_atual(self):
        """
        Deleta o documento selecionado após confirmação do usuário.
        """
        if not self.documento_selecionado:
            return
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar '{self.documento_selecionado.titulo}'?"):
            if self.doc_logic.deletar_documento(self.documento_selecionado.id):
                self._mostrar_visualizador('nao_suportado')
                self.unsupported_label.configure(text="Documento deletado.")
                self.documento_selecionado = None
                self.carregar_lista_de_documentos()
            else:
                messagebox.showerror("Erro", "Não foi possível deletar o documento.")


    def _mostrar_visualizador(self, tipo):
        """
        Alterna entre visualizadores de texto, imagem ou mensagem de não suportado.
        """
        self.textbox.grid_forget()
        self.image_label.grid_forget()
        self.unsupported_label.grid_forget()
        tipos = {
            'texto': lambda: self.textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5)),
            'imagem': lambda: self.image_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        }
        tipos.get(tipo, lambda: self.unsupported_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10))()

    def _visualizar_pdf(self, caminho):
        """
        Exibe a primeira página de um PDF como imagem.
        """
        try:
            doc = fitz.open(caminho)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            doc.close()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            max_size = (self.right_frame.winfo_width() - 40, self.right_frame.winfo_height() - 40)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=img, size=img.size)
            self.image_label.configure(image=ctk_image, text="")
        except Exception as e:
            self._mostrar_visualizador('nao_suportado')
            self.unsupported_label.configure(text=f"Erro ao ler PDF:\n{e}")


    def _visualizar_docx(self, caminho):
        """
        Exibe o conteúdo de um arquivo DOCX no visualizador de texto.
        """
        try:
            doc = docx.Document(caminho)
            texto_completo = [p.text for p in doc.paragraphs]
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", "\n".join(texto_completo))
        except Exception as e:
            self._mostrar_visualizador('nao_suportado')
            self.unsupported_label.configure(text=f"Erro ao ler DOCX:\n{e}")


    def _visualizar_imagem(self, caminho):
        """
        Exibe uma imagem no visualizador de imagens.
        """
        try:
            img = Image.open(caminho)
            max_size = (self.right_frame.winfo_width() - 40, self.right_frame.winfo_height() - 40)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=img, size=img.size)
            self.image_label.configure(image=ctk_image, text="")
        except Exception as e:
            self._mostrar_visualizador('nao_suportado')
            self.unsupported_label.configure(text=f"Erro ao ler imagem:\n{e}")


    def configurar_botoes_e_permissoes(self):
        """
        Configura botões de ação conforme nível de acesso do usuário.
        """
        nivel = self.current_user.nivel_acesso
        action_frame = ctk.CTkFrame(self.right_frame)
        action_frame.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        if nivel in ['Ministro', 'Diretor', 'Servidor']:
            ctk.CTkButton(self.container.winfo_children()[0], text="Novo Documento", command=self.criar_novo_documento).pack(side="bottom", fill="x", padx=5, pady=5)
        if nivel in ['Ministro', 'Diretor']:
            ctk.CTkButton(action_frame, text="Salvar Alterações", command=self.salvar_documento_atual).pack(side="left", padx=10, pady=5)
        if nivel == 'Ministro':
            ctk.CTkButton(action_frame, text="Deletar Documento", command=self.deletar_documento_atual, fg_color="#D9534F").pack(side="left", padx=10, pady=5)


    def logout(self):
        """
        Realiza logout e retorna à tela de login.
        """
        self.container.destroy()
        self.on_logout()