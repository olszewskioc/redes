import socket
import threading


def handle_client(client_socket, client_address, other_server_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f'{username} conectado de {client_address}')

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f'Mensagem recebida | {username}: {message}')
                broadcast(message, client_socket, other_server_socket)

            else:
                remove(client_socket)
                break
    except Exception as e:
        print(f'Erro ao lidar com cliente {client_address} : {e}')
        remove(client_socket)


def broadcast(message, connection, other_server_socket):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
                print(f'Mensagem enviada para {clients[client]}')
            except Exception as e:
                print(f'Erro ao enviar mensagem: {e}')
                remove(client)
    try:
        other_server_socket.send(message.encode('utf-8'))
    except:
        pass


def remove(connection):
    if connection in clients:
        print(f'{clients[connection]} desconectado')
        del clients[connection]


clients = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.7.2', 8080))
server.listen(5)



other_server_ip = '192.168.5.2'
other_server_port = 8080
other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
other_server_socket.connect((other_server_ip, other_server_port))

print('Servidor ON')


while True:
    try:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr, other_server_socket)).start()
        
    except Exception as e:
        print(f'Erro ao aceitar conexão')