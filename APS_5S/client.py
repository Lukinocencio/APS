import socket
from cryptography.fernet import Fernet
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mensageiro Cliente")
        # Configurações
        self.chave = b'NQzcwdHBP1wAT2YoZLmSwIiGV8IztiXUj0Ocu7+7wAI='
        self.fernet = Fernet(self.chave)
        self.PORT = 8888
        self.client_socket = None
        # Solicita o IP do servidor
        self.HOST = self.solicitar_ip()
        if not self.HOST: # Se o usuário cancelar
            self.root.destroy()
            return
        # Configura a interface e conecta ao servidor
        self.configInterface()
        self.cenectServer()

    def solicitar_ip(self):
        """Solicita o IP do servidor através de uma caixa de diálogo"""
        self.root.deiconify() # Mostra a janela principal antes do diálogo
        ip = simpledialog.askstring(
            "Configuração de Conexão",
            "Digite o IP do servidor:",
            parent=self.root,
            initialvalue="192.168.1.5" # Valor padrão
        )
        return ip

    def configInterface(self):
        """Configura os elementos da interface"""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(main_frame, state='disabled')
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        # Entrada de mensagem
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        self.message_entry = tk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.enviaMensagens)
        send_btn = tk.Button(input_frame, text="Enviar", command=self.enviaMensagens)
        send_btn.pack(side=tk.RIGHT)
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set(f"Conectando a {self.HOST}:{self.PORT}...")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)
        # Configuração de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def cenectServer(self):
        """Conecta ao servidor"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))
            self.status_var.set(f"Conectado ao servidor {self.HOST}:{self.PORT}")
            self.caixaMensagem("Sistema", f"Conectado ao servidor {self.HOST}:{self.PORT}")
            # Thread para receber mensagens
            threading.Thread(target=self.reberMensagens, daemon=True).start()
            self.message_entry.focus()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.root.destroy()

    def caixaMensagem(self, sender, message):
        """Exibe mensagem na área de chat"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def reberMensagens(self):
        """Recebe mensagens do servidor"""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = self.fernet.decrypt(data).decode()
                self.root.after(0, self.caixaMensagem, "Servidor", message)
            except Exception as e:
                self.root.after(0, self.caixaMensagem, "Sistema", f"Conexão encerrada: {e}")
                self.root.after(0, lambda: self.status_var.set("Desconectado"))
                break

    def enviaMensagens(self, event=None):
        """Envia mensagem para o servidor"""
        message = self.message_entry.get().strip()
        if not message:
            return
        try:
            encrypted_msg = self.fernet.encrypt(message.encode())
            self.client_socket.sendall(encrypted_msg)
            self.caixaMensagem("Você", message)
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            self.caixaMensagem("Sistema", f"Erro ao enviar mensagem: {e}")
            self.status_var.set("Desconectado")

    def fechar(self):
        """Fecha a conexão ao sair"""
        try:
            if self.client_socket:
                encrypted_msg = self.fernet.encrypt("tt".encode())
                self.client_socket.sendall(encrypted_msg)
                self.client_socket.close()
        except:
            pass
        finally:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # pede o ip, deixando o mensageiro desabilitado
    app = ChatClientGUI(root)
    root.mainloop()
