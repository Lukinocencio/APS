# main.py

"""
Arquivo principal do sistema de reconhecimento facial.
Inicializa o banco de dados, a interface gráfica e o controlador principal.
"""

import customtkinter as ctk
from database.setup import init_db
from controller import AppController

if __name__ == "__main__":
    init_db()
    root = ctk.CTk()
    app = AppController(root)
    root.mainloop()