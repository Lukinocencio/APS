
import customtkinter as ctk
from core.logica import FacialRecognitionLogic
from core.logica_documentos import LogicaDocumentos
from interface.login_screen import LoginScreen
from interface.register_screen import RegisterScreen
from interface.main_screen import MainScreen

class AppController:
    """
    Controlador principal do aplicativo de reconhecimento facial.
    Gerencia a navegação entre telas, inicialização de lógicas e eventos globais.
    """
    def __init__(self, root):
        """
        Inicializa o controlador, configura aparência, centraliza janela e exibe tela de login.
        Args:
            root: Instância da janela principal do Tkinter.
        """
        self.root = root
        self.doc_logic = LogicaDocumentos()
        self.recognition_logic = FacialRecognitionLogic()
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.centralizar_janela(800, 600)
        
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar_app)
        self.current_screen = None
        self.show_login_screen()

    def centralizar_janela(self, width, height):
        """
        Centraliza a janela principal na tela.
        Args:
            width: Largura da janela.
            height: Altura da janela.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _clear_current_screen(self):
        """
        Remove a tela atual do container, se existir.
        """
        if self.current_screen and self.current_screen.container:
            self.current_screen.container.destroy()

    def show_login_screen(self):
        """
        Exibe a tela de login.
        """
        self._clear_current_screen()
        self.current_screen = LoginScreen(
            self.root, 
            self.recognition_logic, 
            on_navigate_to_register=self.show_register_screen,
            on_login_success=self.show_main_screen
        )

    def show_register_screen(self):
        """
        Exibe a tela de registro de usuário.
        """
        self._clear_current_screen()
        self.current_screen = RegisterScreen(
            self.root,
            self.recognition_logic,
            on_registration_complete=self.show_login_screen
        )

    def show_main_screen(self, user):
        """
        Cria e exibe a tela principal após o login.
        Args:
            user: Usuário autenticado.
        """
        self._clear_current_screen()
        
        self.current_screen = MainScreen(
            self.root,
            self.doc_logic,
            user,
            self.show_login_screen
        )

    def ao_fechar_app(self):
        """
        Executa ações de limpeza ao fechar o aplicativo, como parar a câmera.
        """
        if self.recognition_logic:
            self.recognition_logic.parar_camera()
        self.root.destroy()