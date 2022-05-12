import socket
import cv2
import pickle
import struct
import imutils

# [Client Socket]
# Creater an INET, STREAMing socket:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Standard loopback interface address (localhost)
host_ip = '127.0.0.1'
# Port to listen on (non-privleged ports are > 1023)
port = 10050

# Now connet to the web server on the specified port number
client_socket.connect((host_ip, port))
# 'b' or 'B' produces an instance of the bytes type instead of the str type
# used in handling binary data from network connections
# - b"" singifies a bytes string literal 
data = b""
# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")


# [Server Socket]
# Create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_)
host_name = socket.gethostname()
host_ip = socket.gethostname(host_name)
print("HOST IP: ", host_ip)
port = 10050
socket_address = (host_ip, port)
print('Socket created')
# Bind the socket to the host
# The values passed to bind() depend on the address family of the socket
server_socket.bind(socket_address)
print('Socket bind complete')
# listen() enables a server to accept() connections
# listen() has a backlog parameter
# It specifies the number of unnaccepted connections that the system will allow before refusing new connections
server_socket.listen(5)
print('Socket now listening')


# [Server Accepts Client's Request]
while True:
    client_socket, addr = server_socket.accept()
    print('Connection from:', addr)
    if (client_socket):
        vid = cv2.VideoCapture(0)
        while(vid.VideoCapture(0)):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)
            cv2.imshow('Sending...', frame)
            key = cv2.waitKey(10)
            if key == 13:
                client_socket.close()

# [Client Connects to the Server]
while True:
    while(len(data) < payload_size):
        packet = client_socket.recv(4 * 1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("Receiving...", frame)
    key = cv2.waitKey(10)
    if key == 13:
        break

client_socket.close()