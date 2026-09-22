import socket
from cryptography.fernet import Fernet
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

class chatServer:
    def __init__(self, root):
        self.root = root
        self.root.title("mensageiro servidor")
        # Configurações
        self.chave = b'NQzcwdHBP1wAT2YoZLmSwIiGV8IztiXUj0Ocu7+7wAI='
        self.fernet = Fernet(self.chave)
        self.HOST = '0.0.0.0'
        self.PORT = 8888
        self.server_socket = None
        self.listaDCliente = []
        self.selected_client = None
        
        # Inicia interface e servidor
        self.configInterface()
        self.ligarServidor()

    def configInterface(self):
        """Configura a interface gráfica"""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # menu de clientes
        client_frame = tk.Frame(main_frame)
        client_frame.pack(fill=tk.X, pady=5)
        tk.Label(client_frame, text="Cliente:").pack(side=tk.LEFT)
        self.client_combobox = ttk.Combobox(client_frame, state="readonly")
        self.client_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.client_combobox.bind("<<ComboboxSelected>>", self.selectCliente)
        # envio de mensagem
        send_frame = tk.Frame(main_frame)
        send_frame.pack(fill=tk.X, pady=5)
        tk.Label(send_frame, text="Mensagem:").pack(side=tk.LEFT)
        self.message_entry = tk.Entry(send_frame)
        self.message_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.enviarMensagem)
        # Área de log
        self.log_area = scrolledtext.ScrolledText(main_frame, state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True)
        # fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def atualizarListaClientes(self):
        """Atualiza a lista de clientes no combobox"""
        clients = [f"{addr[0]}:{addr[1]}" for conn, addr in self.listaDCliente]
        self.client_combobox['values'] = clients
        if clients and not self.client_combobox.get():
            self.client_combobox.current(0)
            self.selectCliente()

    def selectCliente(self, event=None):
        """Atualiza o cliente selecionado"""
        selection = self.client_combobox.get()
        if selection:
            ip, port = selection.split(':')
            for conn, addr in self.listaDCliente:
                if addr[0] == ip and str(addr[1]) == port:
                    self.selected_client = (conn, addr)
                    self.LogMensagens(f"Cliente selecionado: {addr}")
                    self.message_entry.focus()
                    break

    def LogMensagens(self, message):
        """Adiciona mensagem ao log"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.config(state='disabled')

    def ligarServidor(self):
        """Inicia o servidor automaticamente"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.HOST, self.PORT))
            self.server_socket.listen(5)
            self.LogMensagens(f"Servidor iniciado em {self.HOST}:{self.PORT}")
            # Thread para aceitar conexões
            threading.Thread(target=self.aceitarConexoes, daemon=True).start()
        except Exception as e:
            self.LogMensagens(f"Erro ao iniciar servidor: {e}")
            messagebox.showerror("Erro", f"Não foi possível iniciar o servidor: {e}")
            self.root.destroy()

    def aceitarConexoes(self):
        """Aceita novas conexões de clientes"""
        while True:
            try:
                conn, addr = self.server_socket.accept()
                self.listaDCliente.append((conn, addr))
                self.LogMensagens(f"Novo cliente conectado: {addr}")
                # Atualiza lista de clientes
                self.root.after(0, self.atualizarListaClientes)
                # Thread para lidar com o cliente
                threading.Thread(
                    target=self.gerenciarCliente,
                    args=(conn, addr),
                    daemon=True
                ).start()
            except Exception as e:
                if not isinstance(e, OSError):
                    self.LogMensagens(f"Erro ao aceitar conexão: {e}")
                break

    def gerenciarCliente(self, conn, addr):
        """Lida com a comunicação de um cliente"""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = self.fernet.decrypt(data).decode()
                if msg == "tt":
                    break
                self.LogMensagens(f"{addr} disse: {msg}")
            except Exception as e:
                self.LogMensagens(f"Erro com {addr}: {e}")
                break
        
        conn.close()
        if (conn, addr) in self.listaDCliente:
            self.listaDCliente.remove((conn, addr))
        self.LogMensagens(f"{addr} desconectou")
        self.root.after(0, self.atualizarListaClientes)

    def enviarMensagem(self, event=None):
        """Envia mensagem para o cliente selecionado"""
        if not self.selected_client:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado!")
            return
        message = self.message_entry.get()
        if not message:
            return
        conn, addr = self.selected_client
        try:
            encrypted_msg = self.fernet.encrypt(message.encode())
            conn.sendall(encrypted_msg)
            self.LogMensagens(f"Você para {addr}: {message}")
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            self.LogMensagens(f"Erro ao enviar mensagem: {e}")

    def fechar(self):
        """Fecha o servidor corretamente"""
        try:
            for conn, addr in self.listaDCliente:
                try:
                    conn.close()
                except:
                    pass
            if self.server_socket:
                self.server_socket.close()
            self.root.destroy()
        except Exception as e:
            self.LogMensagens(f"Erro ao fechar servidor: {e}")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = chatServer(root)
    root.mainloop()
