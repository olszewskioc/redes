import socket
import threading

# Função para lidar com clientes
def handle_client(client_socket, client_address):
    try:
        # Receber nome de usuário
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} conectado de {client_address}")
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Mensagem recebida | {username}: {message}")
                broadcast(f"{username}: {message}", client_socket)
            else:
                remove(client_socket)
                break
    except Exception as e:
        print(f"Erro ao lidar com cliente {client_address}: {e}")
        remove(client_socket)

# Função para enviar mensagem a todos os clientes
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
                print(f"Mensagem enviada para {clients[client]}")
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                remove(client)

# Função para remover cliente da lista
def remove(connection):
    if connection in clients:
        print(f"{clients[connection]} desconectado")
        del clients[connection]

# Dicionário de clientes conectados e seus nomes de usuário
clients = {}

# Configurações do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)  # Aumentei o limite de conexões pendentes

print("Servidor iniciado iniciado...")

# Aceitar conexões de clientes
while True:
    try:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")
