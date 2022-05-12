import socket, cv2, pickle, struct, imutils, queue, threading, time, pyshine
from concurrent.futures import ThreadPoolExecutor as TPH

# Create the servers socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# The host name got from the socket module in order to get the ip address
host_name = socket.gethostname()
#host_ip = "10.9.169.204"#socket.gethostbyname(host_name)
host_ip = socket.gethostbyname(host_name)
#host_ip = "0.0.0.0"

print("HOST IP: ", host_ip)
port = 9999

# Completes the socket for the server
socket_address = (host_ip, port)

# Bind the socket
server_socket.bind(socket_address)

# The server socket will listen on the socket--allowing up to 2 people
#server_socket.listen(2)


######################
#       TEXT         #
######################

# Create another socket to handle text
text_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
text_port = 9998

text_socket_address = (host_ip, text_port)

# Bind the text socket
text_socket.bind(text_socket_address)

# # The server socket will listen on the socket--allowing up to 2 people
# text_socket.listen(2)


#client_text_socket_1, addr1 = text_socket.accept()

#client_text_socket_2, addr2 = text_socket.accept()



######################
#       SOUND        #
######################

sound_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sound_port = 9997

sound_socket_address = (host_ip, sound_port)

# Bind the socket
sound_socket.bind(sound_socket_address)


# SOUND COMMUNICATION SOCKET
sound_comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sound_comm_port = 9996

sound_comm_socket_address = (host_ip, sound_comm_port)

# Bind the socket
sound_comm_socket.bind(sound_comm_socket_address)



# The server socket will listen on the socket--allowing up to 2 people
#sound_socket.listen(2)



# Estbalish a dictonary to store each of the clients
# Has an key-value pair of the IP address and a queue of the data for that particular client
#  { "192.168.0.1" : video_image_queue(frame_that_was_sent_over, the_next_frame_to_be_sent_over)}
# [NOTE] The values are currently hardcoded
# queue1 = queue.Queue()
# queue2 = queue.Queue()

client_videos_data = {
                        
                     }


server_socket.listen(1)
print("WAITING FOR CONNECTION ...")
client_socket_1, addr1 = server_socket.accept()
print(f"CLIENT 1 VIDEO SOCKET HAS CONNECTED: {addr1}")
text_socket.listen(1)
client_text_socket_1, addr1 = text_socket.accept()
print(f"CLIENT 1 TEXT SOCKET HAS CONNECTED: {addr1}")
sound_socket.listen(1)
client_sound_socket_1, addr1 = sound_socket.accept()
print(f"CLIENT 1 AUDIO SOCKET HAS CONNECTED: {addr1}")
sound_comm_socket.listen(1)
client_sound_comm_socket_1, addr1 = sound_comm_socket.accept()
print(f"CLIENT 1 AUDIO COMMUNICATION SOCKET HAS CONNECTED: {addr1}")


server_socket.listen(1)
print("WAITING FOR CONNECTION ...")
client_socket_2, addr2 = server_socket.accept()
print(f"CLIENT 2 VIDEO SOCKET HAS CONNECTED: {addr2}")
text_socket.listen(1)
client_text_socket_2, addr2 = text_socket.accept()
print(f"CLIENT 2 TEXT SOCKET HAS CONNECTED: {addr2}")
sound_socket.listen(1)
client_sound_socket_2, addr2 = sound_socket.accept()
print(f"CLIENT 2 AUDIO SOCKET HAS CONNECTED: {addr2}")
sound_comm_socket.listen(1)
client_sound_comm_socket_2, addr2 = sound_comm_socket.accept()
print(f"CLIENT 2 AUDIO COMMUNICATION SOCKET HAS CONNECTED: {addr2}")



client_videos_data[addr1] = queue.Queue()
client_videos_data[addr2] = queue.Queue()


# [!] A SENDING SOCKET WITH ITS OWN DEDICATED PORT
# sending_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sending_port = 9998
# sending_socket.connect((addr1[0], sending_port))





# [!] Two threads for each client
# [!] one thread put data into the dictonary
# [!] one thread take data out of the dictonary and forward it to the next client

# Create a lock for the threads to use
lock = threading.Lock()


def forward_audio_thread(audio_socket_1, audio_socket_2, client_sound_comm_socket_1, thread_id):
    # while True:
    #     sound = text_socket_1.recv(4*1024)

    #     text_socket_2.sendall(b"sound HERE")

    #     #print("IN FORWARD AUDIO [server]")
    #     print(sound)
    print("THIS IS IN FORWARD AUDIO")


    # Data to store the bytestring
    data = b""

    # https://searchsecurity.techtarget.com/definition/payload
    # A payload is needed for a packet
    # [Payload] - The carrying capacity of a packet or other transmission data unit.
    # struct.calcsize("Q") calculates an unsigned long long size with a given integer; the standard size for "Q" is 8
    packet_payload = struct.calcsize("Q")


    audio, context = pyshine.audioCapture(mode="get")

    isMuted = False

    while True:
        #print ("[forward audio thread]")

        # If there is a connection
        if audio_socket_1:
            # [test]
            # muted = client_sound_comm_socket_1.recv(5).decode()
            # print(f"MUTED {muted}")
            # if muted == "True":
            #     print("IN IF CASE")
            #     isMuted = True
            # elif muted == "False":
            #     print("IN ELIF CASE")
            #     isMuted = False
            
            # IF THE CLIENT IS MUTED
            if isMuted:
                print("CLIENT IS MUTED")
                pass
            
            elif not isMuted:
                print("RECEIVING AUDIO")
                # [TESTING VIDEO COMIPLATION ON SERVER SIDE - RECIEVING END]
                while len(data) < packet_payload:
                    packet = audio_socket_1.recv(4*1024)
                    if not packet: break
                    data += packet
                    print("UNPACKAGING DATA")
                packed_msg_size = data[:packet_payload]
                data = data[packet_payload:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += audio_socket_1.recv(4*1024)
                    #print("len(data): ", len(data), "msg_size: ", msg_size)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                #frame = pickle.loads(frame_data)

                frame = struct.pack("Q", len(frame_data)) + frame_data
                audio_socket_2.sendall(frame)
                #print(frame)

                #audio.put(frame)

                
                #with lock:
                    #client_videos_data[address].put(frame_data)
                    #print("HELLO WORLD")

            
                # key = cv2.waitKey(1) & 0xFF
                
                # if key == ord('q'):
                #     break
        
    print("outside while loop")
    audio_socket_1.close()




def forward_text_thread(text_socket_1, text_socket_2, address, thread_id):
    while True:
       text = text_socket_1.recv(4*1024)

       text_socket_1.sendall(text)
       text_socket_2.sendall(text)
       #text_socket.sendall(text)


       print(text)




########################################################################
######################### IMPORTING THREAD #############################
########################################################################


# Thread that places data into the dictonary with ADDR : queue pair
def importing_thread(client_socket, address, thread_id):#image):
    print(f"ADDRESS: {address}, client_socket: {client_socket}")

    # Data to store the bytestring
    data = b""

    # https://searchsecurity.techtarget.com/definition/payload
    # A payload is needed for a packet
    # [Payload] - The carrying capacity of a packet or other transmission data unit.
    # struct.calcsize("Q") calculates an unsigned long long size with a given integer; the standard size for "Q" is 8
    packet_payload = struct.calcsize("Q")




    
    while True:
       # print ("[importing_thread]")

        # If there is a connection
        if client_socket:
            # Place the IP address of int the client_videos_data dictonary with an empty queue
            # if it has not been placed there before
            # if address not in client_videos_data:
            #     client_videos_data[address] = queue.Queue()
            # [TESTING VIDEO COMIPLATION ON SERVER SIDE - RECIEVING END]
            while len(data) < packet_payload:
                packet = client_socket.recv(4*1024)
                #print("len(data): ", len(data), "packet_payload: ", packet_payload)
                if not packet: break
                data += packet
            packed_msg_size = data[:packet_payload]
            data = data[packet_payload:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
                #print("len(data): ", len(data), "msg_size: ", msg_size)
            frame_data = data[:msg_size]
            data  = data[msg_size:]

            
            with lock:
                client_videos_data[address].put(frame_data)

           # frame = pickle.loads(frame_data)
           # print(f"framelen: {len(frame)}")
        

           # cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key  == ord('q'):
                break
        
    print("outside while loop")
    client_socket.close()


########################################################################
######################### EXPORTING THREAD #############################
########################################################################


# def exporting_thread(thread_id):
    
#     # Run this thread idefinately
#     while True:
#         print ("[exporting_thread] IN WHILE LOOP MAY NOT HAVE LOCK")
#         with lock:
#             # [!] TEST!
#             #time.sleep(5)
#             #print(f"THIS IS A EXPORT THREAD {thread_id}")

#             data_to_forward = client_videos_data["192.0.0.1"].get()

#             print(f"THREAD{thread_id} WILL EXPORT THIS DATA: {data_to_forward}")

#         #Code to forward the data to a given client


def exporting_thread(client_socket, address, thread_id,):#image):
    """
    client_socket - Client to forward to
    """
    while True:
       # print ("[exporting_thread]")
        #print(f"client videos: {client_videos_data[address].get()}")

        with lock:
           # print(f"[exporting_thread- LOCK]")
            if not client_videos_data[address].empty():
                data_to_forward = client_videos_data[address].get()


                #print(f"data_to_forward_size: {len(data_to_forward)}")
                data_to_forward = struct.pack("Q", len(data_to_forward)) + data_to_forward               

                #sending_socket.sendall(b"testing 123 sending data")
               # sending_socket.sendall(data_to_forward)
                client_socket.sendall(data_to_forward)
                



            #print(f"IN LOCK")




# [MAIN THREAD]
# - Keeps the server running!
# - If a connection is accepted import and export threads are created for that client to handle the dictonary
# - Uses data from a client and sends that data along with that address to a import_to_dict thread
# - Stores the connected addresses to be accessed later


# [!] MAY CONSIDER MOVING THIS CODE OUTSIDE OF WHILE LOOP AS THE WHILE LOOP IS ONLY KEEPING THE SERVER ALIVE

with TPH(max_workers=8) as executor:
    # Create thread for handling imports for client_socket_1
    executor.submit( importing_thread, client_socket_1, addr1, 1)
    # Create thread for handling exports for client_socket_1
    executor.submit( exporting_thread, client_socket_2, addr1, 1)


    # Create thread for handling imports for client_socket_2
    executor.submit( importing_thread, client_socket_2, addr2, 2)
    # Create thread for handling exports for client_socket_2
    executor.submit( exporting_thread, client_socket_1, addr2, 2)

    # Text threads
    executor.submit(forward_text_thread, client_text_socket_1, client_text_socket_2, addr2, 1)
    executor.submit(forward_text_thread, client_text_socket_2, client_text_socket_1, addr2, 2)
    #executor.submit(forward_text_thread, client_text_socket_2, addr1, 2)


    executor.submit(forward_audio_thread, client_sound_socket_1, client_sound_socket_2, client_sound_comm_socket_1, 1)
    executor.submit(forward_audio_thread, client_sound_socket_2, client_sound_socket_1, client_sound_comm_socket_2, 2)

print("HELLO WORLD")
# KEEPS THE SERVER ALIVE
while True:
    # IN MAIN LOOP
    #print("IN MAIN LOOP")
    pass




    






        
