
# interface/register_screen.py

"""
Tela de cadastro de usuário do sistema de reconhecimento facial.
Permite inserir dados, capturar fotos e treinar modelo biométrico.
"""

import customtkinter as ctk
from tkinter import messagebox, StringVar
from PIL import Image
import cv2
import time

class RegisterScreen:
    """
    Tela de cadastro de usuário, incluindo captura de fotos e treinamento do modelo.
    """
    def __init__(self, root, logic, on_registration_complete):
        """
        Inicializa a tela de cadastro e variáveis de controle.
        Args:
            root: Janela principal do Tkinter.
            logic: Lógica de reconhecimento facial.
            on_registration_complete: Função chamada ao finalizar cadastro.
        """
        self.root = root
        self.logic = logic
        self.on_registration_complete = on_registration_complete
        self.container = ctk.CTkFrame(root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.dados_usuario_em_cadastro = {}
        self.fotos_capturadas_em_memoria = []
        self.NUM_FOTOS_PARA_CAPTURAR = 30
        self.INTERVALO_CAPTURA_SEGUNDOS = 0.05
        self.captura_iniciada = False
        self.proxima_captura_time = 0
        self.mostrar_tela_formulario_cadastro()


    def _validar_cpf(self, P):
        """
        Valida se o CPF contém apenas dígitos e até 11 caracteres.
        """
        if P == "":
            return True
        if P.isdigit() and len(P) <= 11:
            return True
        return False

    def mostrar_tela_formulario_cadastro(self):
        """
        Exibe o formulário para cadastro de dados do novo usuário.
        AGORA: Preenche os campos se os dados já existirem.
        """
        self._limpar_tela()
        self.root.title("Cadastro - Passo 1: Informações")
        frame_form = ctk.CTkFrame(self.container)
        frame_form.pack(fill="both", expand=True, padx=50, pady=50)
        frame_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_form, text="Dados do Novo Usuário", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=2, pady=20)
        ctk.CTkLabel(frame_form, text="Nome:").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Digite o nome completo", height=35)
        self.entry_nome.grid(row=1, column=1, sticky="ew", padx=20, pady=10)

        ctk.CTkLabel(frame_form, text="CPF:").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.entry_cpf = ctk.CTkEntry(frame_form, placeholder_text="Digite 11 números", height=35)
        self.entry_cpf.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        vcmd = (self.root.register(self._validar_cpf), '%P')
        self.entry_cpf.configure(validate="key", validatecommand=vcmd)
        
        ctk.CTkLabel(frame_form, text="Nível de Acesso:").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        niveis = ["Ministro", "Diretor", "Servidor"]

        nivel_salvo = self.dados_usuario_em_cadastro.get("nivel_acesso", niveis[-1])
        self.nivel_acesso_var = StringVar(value=nivel_salvo)


        ctk.CTkComboBox(frame_form, variable=self.nivel_acesso_var, values=niveis, height=35, state="readonly").grid(row=3, column=1, sticky="w", padx=20, pady=10)
        

        if self.dados_usuario_em_cadastro.get("nome"):
            self.entry_nome.insert(0, self.dados_usuario_em_cadastro.get("nome"))
        if self.dados_usuario_em_cadastro.get("cpf"):
            self.entry_cpf.insert(0, self.dados_usuario_em_cadastro.get("cpf"))


        btn_frame = ctk.CTkFrame(frame_form, fg_color="transparent"); btn_frame.grid(row=4, column=0, columnspan=2, pady=30)
        ctk.CTkButton(btn_frame, text="Continuar", command=self.iniciar_captura_handler, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Voltar", command=self._finalizar_e_voltar, fg_color="gray50", height=40).pack(side="left", padx=10)

    def iniciar_captura_handler(self):
        """
        Valida dados do formulário e inicia captura de fotos.
        """
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return
        if len(cpf) != 11:
            messagebox.showwarning("Atenção", "O CPF deve conter exatamente 11 dígitos.")
            return
        self.dados_usuario_em_cadastro = {"nome": nome, "cpf": cpf, "nivel_acesso": self.nivel_acesso_var.get()}
        self.fotos_capturadas_em_memoria = []
        self.mostrar_tela_captura()


    def _limpar_tela(self):
        """
        Remove todos os widgets da tela atual.
        """
        for widget in self.container.winfo_children():
            widget.destroy()


    def _finalizar_e_voltar(self):
        """
        Finaliza cadastro e retorna à tela anterior.
        """
        self.logic.parar_camera()
        self.container.destroy()
        self.on_registration_complete()


    def mostrar_tela_captura(self):
        """
        Exibe tela de captura automática de fotos para biometria.
        """
        self._limpar_tela()
        self.root.title("Cadastro - Passo 2: Captura Automática de Fotos")
        
        self.modelo_pronto_para_verificacao = self.logic.preparar_acesso()
        if self.modelo_pronto_para_verificacao:
            print("INFO: Modelo de verificação carregado. Rostos existentes serão detectados.")
        else:
            print("INFO: Nenhum modelo de treinamento encontrado. A verificação de rosto existente está desativada.")
        self.nome_rosto_detectado = None
        self.logic.iniciar_camera()

        self.fotos_capturadas_em_memoria = []
        self.captura_iniciada = True
        frame_cam = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_cam.pack(fill="both", expand=True)
        self.label_video = ctk.CTkLabel(frame_cam, text="")
        self.label_video.pack(pady=10)
        self.label_info = ctk.CTkLabel(frame_cam, text="Centralize um único rosto no quadro para iniciar a captura", font=ctk.CTkFont(size=14))
        self.label_info.pack(pady=10)
        try:
            self._label_info_default_color = self.label_info.cget("text_color")
        except Exception:
            self._label_info_default_color = None


        self.progress_bar = ctk.CTkProgressBar(frame_cam, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self._atualizar_frame_cadastro()

        ctk.CTkButton(
            frame_cam,
            text="Voltar ao Formulário",
            command=self._voltar_para_formulario,
            fg_color="gray50",
            height=40
        ).pack(pady=(20, 10))
        

    def _atualizar_frame_cadastro(self):
        """
        Atualiza o frame de vídeo, verifica em tempo real se o rosto já está
        cadastrado e atualiza a interface de acordo, sem interromper o vídeo.
        """
        if not hasattr(self, 'label_video') or not self.label_video.winfo_exists():
            return
        
        frame = self.logic.current_frame
        if frame is None:
            if self.container.winfo_exists():
                self.root.after(33, self._atualizar_frame_cadastro)
            return

        frame_para_exibir = frame.copy()
        frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.logic.detector_face.detectMultiScale(frame_cinza, 1.3, 5)


        self.nome_rosto_detectado = None
        if self.modelo_pronto_para_verificacao and len(faces) == 1:
            (x, y, w, h) = faces[0]
            rosto_a_verificar = frame_cinza[y:y+h, x:x+w]

            self.nome_rosto_detectado = self.logic.verificar_rosto_existente(rosto_a_verificar)


        cor_retangulo = (255, 0, 0) 
        

        if self.nome_rosto_detectado:
            cor_retangulo = (0, 0, 255) 

        for (x, y, w, h) in faces:
            cv2.rectangle(frame_para_exibir, (x, y), (x + w, y + h), cor_retangulo, 2)

        img = cv2.cvtColor(frame_para_exibir, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img)
        ctk_image = ctk.CTkImage(light_image=pil_image, size=pil_image.size)
        self.label_video.configure(image=ctk_image)
        self.label_video.image = ctk_image

        rosto_processado = self.logic.processar_rosto_para_captura()

        if self.nome_rosto_detectado:
            self.label_info.configure(
                text=f"ERRO: Rosto já pertence a {self.nome_rosto_detectado}",
                text_color="red"
            )
            progresso = len(self.fotos_capturadas_em_memoria) / self.NUM_FOTOS_PARA_CAPTURAR
            self.progress_bar.set(progresso)

        elif self.captura_iniciada and rosto_processado is not None:
            agora = time.time()
            if agora > self.proxima_captura_time:
                self.proxima_captura_time = agora + self.INTERVALO_CAPTURA_SEGUNDOS
                self.fotos_capturadas_em_memoria.append(rosto_processado)
                num_fotos = len(self.fotos_capturadas_em_memoria)
                progresso = num_fotos / self.NUM_FOTOS_PARA_CAPTURAR
                self.progress_bar.set(progresso)
                self.label_info.configure(text="Mantenha a posição, estamos cadastrando você...", text_color="blue")
                
                if num_fotos >= self.NUM_FOTOS_PARA_CAPTURAR:
                    self.captura_iniciada = False
                    self._finalizar_processo_de_cadastro()
        else:
            self.label_info.configure(
                text="Centralize um único rosto no quadro para capturar",
                text_color=self._label_info_default_color
            )

        if self.container.winfo_exists():
            self.root.after(33, self._atualizar_frame_cadastro)

    def _finalizar_processo_de_cadastro(self):
        """
        Finaliza cadastro, salva usuário e fotos, treina modelo e retorna.
        """
        self.logic.parar_camera()
        self.label_info.configure(text="Processando cadastro, por favor aguarde...")
        novo_usuario = self.logic.salvar_e_obter_usuario(**self.dados_usuario_em_cadastro)
        if not novo_usuario:
            cpf_salvo = self.dados_usuario_em_cadastro.get('cpf', 'N/A')
            messagebox.showerror("Erro", f"O CPF '{cpf_salvo}' já está cadastrado.")
            self._finalizar_e_voltar()
            return
        self.logic.salvar_fotos_capturadas(novo_usuario.id, self.fotos_capturadas_em_memoria)
        messagebox.showinfo("Sucesso", f"{self.NUM_FOTOS_PARA_CAPTURAR} fotos capturadas e usuário salvo! Iniciando treinamento...")
        if self.logic.treinar_modelo():
            messagebox.showinfo("Treinamento", "Modelo treinado com sucesso!")
        else:
            messagebox.showerror("Treinamento", "Falha ao treinar o modelo.")
        self._finalizar_e_voltar()


    def _voltar_para_formulario(self):
        """
        Para a câmera e retorna para a tela do formulário de cadastro,
        mantendo os dados preenchidos.
        """
        print("Ação: Voltando para o formulário de cadastro.")
        self.logic.parar_camera()
        self.mostrar_tela_formulario_cadastro()