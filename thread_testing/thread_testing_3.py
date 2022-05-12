import threading
import time
from concurrent.futures import ThreadPoolExecutor as TPH


# def thread_function(name):
#     print(f"Thread {name}: starting")
#     time.sleep(2)
#     print(f"Thread {name}: finishing")


lock = threading.Lock()


# A infinite while loop that prints a value
def infinite_thread(thread_number):
    while True:
        with lock:
            print(f"Regular Thread Number: {thread_number}")

def another_infinite_thread(thread_number):
    while True:
        with lock:
            print(f"Special Thread Number: {thread_number}")
            time.sleep(1)

#shareResource = 75
# def modifyResource():
#     global shareResource
#     shareResource += 1
#     print(shareResource)


with TPH(max_workers=4) as executor:
    executor.submit(infinite_thread, 1)
    executor.submit(infinite_thread, 2)

    executor.submit(another_infinite_thread, 1)
    executor.submit(another_infinite_thread, 2)


#print(shareResource)



   