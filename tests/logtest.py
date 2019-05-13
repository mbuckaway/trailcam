import logging
import threading
import os
import time
from webcamlib.ConfigureLogging import logging_setup


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("test-{}-{}".format(name, threadID))
        self.threadID = threadID
        self.name = name
    def run(self):
        self.logger.info("Starting " + self.name)
        for item in range(100000):
            self.logger.info("Test line {}".format(item))
            time.sleep(.1)
        self.logger.info("Exiting " + self.name)

"""
Not really a unit test, but a test to test out logging configuration and log rotation.
Ran into some errors when a log was to be rotated
"""
def main():
    logging_setup("test.log", 'DEBUG', True, True)
    logger = logging.getLogger("main")
    logger.info("Starting Main Thread")

    threads = []

    # Create new threads
    thread1 = myThread(1, "Thread-1")
    thread2 = myThread(2, "Thread-2")
    thread3 = myThread(3, "Thread-3")

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    logger.info("Exiting Main Thread")


if __name__ == '__main__':
    main()
