import logging
import threading
import time

# def thread_function(name):
#     logging.info(f"Thread {name}: starting")
#     time.sleep(2)
#     logging.info(f"Thread {name}: finishing")

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     logging.info("Main    : before creating thread")

#     x = threading.Thread(target=thread_function, args=(1,), daemon=True)
#     logging.info("Main : before running thread")
#     x.start()
#     logging.info("Main : wait for the thread to finish")
#     # The main thread will pause and wait for the thread x to complete running
#     x.join()
#     logging.info("Main : all done")

from concurrent.futures import ThreadPoolExecutor as TPH

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)

        # USE THE LOCK
        with self._lock:
            logging.debug("Thread %s has the lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release the lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

class FakeDatabase_old:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.info(f"Testing update. Starting value is {database.value}")
    with TPH(max_workers=2) as exectutor:
        for index in range(2):
            exectutor.submit(database.update, index)
    logging.info(f"testing update. Ending value is {database.value}")