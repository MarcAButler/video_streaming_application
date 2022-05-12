from queue import Queue

queue1 = Queue()

client_data = {
                "192.0.0.1" : queue1

              }

addr = "192.0.0.1"

client_data[addr].put("T232131")

print(client_data[addr].get())