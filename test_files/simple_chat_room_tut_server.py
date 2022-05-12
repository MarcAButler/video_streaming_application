# import socket
# import select
# import sys
# from _thread import *

# """The first argument AF_INET is the address domain of the
# socket. This is used when we have an Internet Domain with
# any two hosts The second argument is the type of socket.
# SOCK_STREAM means that data or characters are read in
# a continuous flow."""
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# # Checks whether sufficient arguments have been provided
# if len(sys.argv) != 3:
#     print("Correct Usage: script, IP address, port number")
#     exit()

# # Takes the first argument from the command prompt as IP address
# IP_address = str(sys.argv[1])

# # Takes the second argument from the command as the port number
# Port = int(sys.argv[2])

# """
# Binds the server to an entered IP address and at the specified port number.
# The client must be aware of these parameters
# """
# server.bind((IP_address, Port))

# """
# Listens for 100 active connections. This number can be increased as per convience.
# """
# server.listen(100)

# list_of_clients = []

# def clientthread(conn, addr):

#     # Sends a message to the client whose user object is conn
#     conn.send("Welcome to this chatroom!")

#     while True:
#         try:
#             message = conn.recv(4096)
#             if message:
#                 """Prints the message and address of the user who just sent the message on the server terminal"""
#                 print("<" + addr[0] + "> " + message)

#                 # Calls broadcast function to send message to all
#                 message_to_send = "<" + addr[0] + "> " + message
#                 broadcast(message_to_send, conn)

#             else:
#                 """Message may have no content if the connection is broken, in this case we remove the connection"""
#                 remove(conn)
#         except:
#             continue

# """Using the below function, we boradcast the message to all clients who's object is not the same as the one sending the message"""
# def broadcast(message, connection):
#     for clients in list_of_clients:
#         if clients != connection:
#             try: 
#                 clients.send(message)
#             except:
#                 clients.close()
#                 # If the link is broken we remove the client

# """The following function simply removes the object from the list that was created at the beginning of the program"""
# def remove(connection):
#     if connection in list_of_clients:
#         list_of_clients.remove(connection)

# while True:
    
#     """Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains the IP address of the client that just connected to the server"""
#     conn, addr = server.accept()

#     """Maintains a list of clients for ease of broadcasting a message to all available people in the chatroom"""
#     list_of_clients.append(conn)

#     # Prints the address of the user that just connected
#     print(addr[0] + " connected")

#     # Creates and individual thread for every user that connects
#     start_new_thread(clientthread, (conn, addr))

# conn.close()
# server.close()


import socket
import select
from threading import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!")
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message
                    broadcast(message_to_send,conn)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects

conn.close()
server.close()