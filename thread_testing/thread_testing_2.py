import threading
import time
from concurrent.futures import ThreadPoolExecutor as TPH


# def thread_function(name):
#     print(f"Thread {name}: starting")
#     time.sleep(2)
#     print(f"Thread {name}: finishing")



shareResource = 75

def modifyResource():
    global shareResource
    shareResource += 1
    print(shareResource)


with TPH(max_workers=5) as executor:
    executor.submit(modifyResource)
    executor.submit(modifyResource)

print(shareResource)



   