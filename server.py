from ipaddress import ip_address
import socket
from threading import Thread

from numpy import broadcast
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()

list_of_clients= []
nicknames = []
print("SERVER HAS STARTED")

def ClientThread(conn,addr):
    conn.send("welcome to this chat room".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')

            if message:
                print(message)
                broadcast(message,conn)
            else:

                remove(conn)
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode("utf-8"))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
while True:
    conn,addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} Joined".format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target = ClientThread, args=(conn,nickname))
    new_thread.start()