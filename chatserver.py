import socket
import threading
import time


clients = []
nicknames = []



def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}: {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = "localhost"
    server.bind((host, 5560))
    server.listen()
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        print(f"client's name is " + nickname)
        connected_clients="NEWCONN"


        clients.append(client)
        nicknames.append(nickname)
        for i in nicknames:
            connected_clients = connected_clients + " "+ i
        print(connected_clients)
        connected_clients = connected_clients+"$"
        broadcast(connected_clients.encode('utf-8'))

        broadcast(f"CHAT {nickname} connected to the server!\n$".encode('utf-8'))
        client.send("CHAT You are now connected to the server\n$".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
print("server running")