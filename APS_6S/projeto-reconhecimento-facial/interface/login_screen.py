
# interface/login_screen.py

"""
Tela de login do sistema de reconhecimento facial.
Permite ao usuário acessar via biometria facial ou navegar para cadastro.
Gerencia interface, eventos e integração com lógica de reconhecimento.
"""

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import cv2

class LoginScreen:
    def __init__(self, root, logic, on_navigate_to_register, on_login_success):
        """
        Inicializa a tela de login.
        Args:
            root: Janela principal do Tkinter.
            logic: Instância da lógica de reconhecimento facial.
            on_navigate_to_register: Função para navegação ao cadastro.
            on_login_success: Função chamada após login bem-sucedido.
        """
        self.root = root
        self.logic = logic
        self.on_navigate_to_register = on_navigate_to_register
        self.on_login_success = on_login_success

        self.container = ctk.CTkFrame(root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.acesso_after_id = None
        self.timer_acesso_iniciado = False
        self.criar_tela_inicial()

    def _limpar_tela(self):
        """
        Remove todos os widgets da tela atual.
        """
        for widget in self.container.winfo_children():
            widget.destroy()

    def criar_tela_inicial(self):
        """
        Cria a tela inicial de boas-vindas e opções de login/cadastro.
        """
        self._limpar_tela()
        self.root.title("Sistema de Acesso Ambiental")

        frame_principal = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True)

        login_frame = ctk.CTkFrame(frame_principal, corner_radius=15, border_width=2)
        login_frame.pack(expand=True)

        ctk.CTkLabel(login_frame, text="Sistema de Acesso", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30, padx=60)
        ctk.CTkButton(login_frame, text="Cadastrar Usuário", command=self.on_navigate_to_register, width=200, height=40).pack(pady=15, padx=40)
        ctk.CTkButton(login_frame, text="Acessar com Biometria", command=self.mostrar_tela_acesso, width=200, height=40).pack(pady=(15, 30), padx=30)

    def mostrar_tela_acesso(self):
        """
        Cria a tela de acesso facial e inicia a câmera para reconhecimento.
        """
        if not self.logic.preparar_acesso():
            messagebox.showerror("Erro", "Nenhum modelo treinado encontrado.")
            return

        self._limpar_tela()
        self.root.title("Acesso - Reconhecimento Facial")
        self.logic.iniciar_camera()

        self.timer_acesso_iniciado = False
        if self.acesso_after_id:
            self.root.after_cancel(self.acesso_after_id)

        frame_acesso = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_acesso.pack(fill="both", expand=True, pady=20)

        self.label_video_acesso = ctk.CTkLabel(frame_acesso, text="")
        self.label_video_acesso.pack(pady=10, padx=20)

        self.label_info_acesso = ctk.CTkLabel(frame_acesso, text="Posicione o rosto para a câmera", font=ctk.CTkFont(size=14))
        self.label_info_acesso.pack(pady=10)

        ctk.CTkButton(frame_acesso, text="Cancelar e Voltar", command=self._voltar_da_tela_acesso, fg_color="gray50").pack(pady=20)

        self._atualizar_frame_acesso()

    def _atualizar_frame_acesso(self):
        """
        Atualiza o frame de vídeo e status do reconhecimento facial em tempo real.
        """
        if not hasattr(self, 'label_video_acesso') or not self.label_video_acesso.winfo_exists(): 
            return

        frame, usuario = self.logic.reconhecer_rosto()

        if frame is not None:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img)
            ctk_image = ctk.CTkImage(light_image=pil_image, size=pil_image.size)
            self.label_video_acesso.configure(image=ctk_image)
            self.label_video_acesso.image = ctk_image

        if usuario and not self.timer_acesso_iniciado:
            self.timer_acesso_iniciado = True
            self.label_info_acesso.configure(text=f"Bem-vindo, {usuario.nome}!", text_color="green", font=ctk.CTkFont(weight="bold"))
            self.acesso_after_id = self.root.after(3000, lambda u=usuario: self._conceder_acesso(u))
        elif not usuario and self.timer_acesso_iniciado:
            self.timer_acesso_iniciado = False
            self.label_info_acesso.configure(text="Rosto não reconhecido.", text_color="red", font=ctk.CTkFont(weight="normal"))
            if self.acesso_after_id: 
                self.root.after_cancel(self.acesso_after_id)

        if self.container.winfo_exists(): 
            self.root.after(33, self._atualizar_frame_acesso)

    def _conceder_acesso(self, usuario):
        """
        Finaliza o reconhecimento facial e concede acesso ao usuário.
        Args:
            usuario: Usuário reconhecido.
        """
        self.logic.parar_camera()
        self.container.destroy()
        self.on_login_success(usuario)

    def _voltar_da_tela_acesso(self):
        """
        Cancela o acesso facial e retorna à tela inicial.
        """
        self.logic.parar_camera()
        if self.acesso_after_id:
            self.root.after_cancel(self.acesso_after_id)
        self.criar_tela_inicial()