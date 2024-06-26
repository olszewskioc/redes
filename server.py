import socket
import threading

# Função para lidar com clientes
def handle_client(client_socket, client_address, other_server_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} conectado de {client_address}")
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received from {username}: {message}")
                broadcast(message, client_socket, other_server_socket)
            else:
                remove(client_socket)
                break
    except:
        remove(client_socket)

# Função para enviar mensagem a todos os clientes e ao outro servidor
def broadcast(message, connection, other_server_socket):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)
    # Enviar mensagem ao outro servidor
    try:
        other_server_socket.send(message.encode('utf-8'))
    except:
        pass

# Função para remover cliente da lista
def remove(connection):
    if connection in clients:
        print(f"{clients[connection]} desconectado")
        del clients[connection]

clients = {}

# Configurações do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))  # Escuta em todas as interfaces na porta 5555
server.listen(5)

# Conectar ao outro servidor
other_server_ip = 'IP_DO_OUTRO_SERVIDOR'
other_server_port = 5555
other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
other_server_socket.connect((other_server_ip, other_server_port))

print("Servidor iniciado...")

# Aceitar conexões de clientes
while True:
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr, other_server_socket)).start()
