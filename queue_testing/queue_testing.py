import queue


address = "192.128.0.1"

client_videos_data = {}

client_videos_data[address] = queue.Queue()


for i in range(10):
    client_videos_data[address].put(i)


for i in range(10):
    val = client_videos_data[address].get()
    print(val)