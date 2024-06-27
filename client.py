import socket
import threading
from tkinter import *
from tkinter import simpledialog, messagebox

# Função para receber mensagens do servidor
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                message_list.insert(END, message)
                message_list.yview(END)
        except OSError:  # Cliente foi desconectado
            break

# Função para enviar mensagens ao servidor
def send(event=None):
    try:
        message = my_message.get()
        my_message.set("")
        formatted_message = f"Eu: {message}"
        message_list.insert(END, formatted_message)
        message_list.yview(END)
        client.send(f"{message}".encode('utf-8'))
    except OSError:  # Caso de erro no envio
        messagebox.showerror("Erro", "Falha ao enviar a mensagem. Conexão perdida.")

# Função para fechar a janela do cliente e desconectar
def on_closing(event=None):
    my_message.set("QUIT")
    send()
    client.close()
    root.quit()

# Configurações da GUI
root = Tk()
root.title("Chat Cliente")

messages_frame = Frame(root)
my_message = StringVar()
my_message.set("Digite sua mensagem...")
scrollbar = Scrollbar(messages_frame)
message_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
message_list.pack(side=LEFT, fill=BOTH)
message_list.pack()
messages_frame.pack()

entry_field = Entry(root, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(root, text="Enviar", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

# Solicitar o nome de usuário
username = simpledialog.askstring("Nome de Usuário", "Digite seu nome de usuário:", parent=root)
if not username:
    messagebox.showerror("Erro", "Nome de usuário é obrigatório.")
    root.quit()

# Configurações do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tratamento de exceções na conexão ao servidor
try:
    # Substitua 'IP_DO_SERVIDOR_LOCAL' pelo IP correto do servidor local
    client.connect(('192.168.7.2', 8080))
    client.send(username.encode('utf-8'))  # Enviar nome de usuário ao servidor
except ConnectionRefusedError:
    messagebox.showerror("Erro de Conexão", "Falha ao conectar ao servidor. Verifique o IP e a porta e tente novamente.")
    root.quit()
except socket.gaierror:
    messagebox.showerror("Erro de Conexão", "Endereço IP inválido. Verifique e tente novamente.")
    root.quit()
except Exception as e:
    messagebox.showerror("Erro de Conexão", f"Ocorreu um erro: {e}")
    root.quit()

# Thread para receber mensagens
threading.Thread(target=receive).start()

root.mainloop()