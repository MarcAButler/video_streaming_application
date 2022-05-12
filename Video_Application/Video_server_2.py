import socket, cv2, pickle, struct, imutils, queue, threading

# Create the servers socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# The host name got from the socket module in order to get the ip address
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

print("HOST IP: ", host_ip)
port = 9999

# Completes the socket for the server
socket_address = (host_ip, port)

# Bind the socket
server_socket.bind(socket_address)

# The server socket will listen on the socket--allowing up to 2 people
server_socket.listen(2)





# Estbalish a dictonary to store each of the clients
# Has an key-value pair of the IP address and a queue of the data for that particular client
#  { "192.168.0.1" : video_image_queue(frame_that_was_sent_over, the_next_frame_to_be_sent_over)}
# [NOTE] The values are currently hardcoded
queue1 = queue.Queue()
queue2 = queue.Queue()

client_videos_data = {
                        
                     }


# https://searchsecurity.techtarget.com/definition/payload
# A payload is needed for a packet
# [Payload] - The carrying capacity of a packet or other transmission data unit.
# struct.calcsize("Q") calculates an unsigned long long size with a given integer; the standard size for "Q" is 8
packet_payload = struct.calcsize("Q")

# Data to store the bytestring
data = b""




client_socket, addr = server_socket.accept()
print(type(addr))
client_socket_2, addr = server_socket.accept()


      

# [!] Two threads for each client
# [!] one thread put data into the dictonary
# [!] one thread take data out of the dictonary and forward it to the next client


# Create a lock for the threads to use
lock = threading.Lock()

# [MAIN THREAD]



# Thread that places data into the dictonary with ADDR : queue pair
def importing_thread(client_socket, image):
        # Constantly accept incoming connections
    while True:


        # If there is a connection
        if client_socket:
            # Place the IP address of int the client_videos_data dictonary with an empty queue
            # if it has not been placed there before
            if addr not in client_videos_data:
                client_videos_data[addr] = queue.Queue()
            # [TESTING VIDEO COMIPLATION ON SERVER SIDE - RECIEVING END]
            while len(data) < packet_payload:
                packet = client_socket.recv(4*1024)
                print("len(data): ", len(data), "packet_payload: ", packet_payload)
                if not packet: break
                data += packet
            packed_msg_size = data[:packet_payload]
            data = data[packet_payload:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
                print("len(data): ", len(data), "msg_size: ", msg_size)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            with lock:
                client_videos_data[addr] = queue1.put(image)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            print("in while loop")
            if key  == ord('q'):
                break
        
    print("outside while loop")
    client_socket.close()

        
def exporting_thread(image):
    with lock:
        data_to_forward = client_videos_data["192.0.0.1"].get()

        # Code to forward the data to a given client


