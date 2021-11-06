import atexit
import time


def exit_handler():
    print("exit...")


atexit.register(exit_handler)

while True:
    print("waiting....")
    time.sleep(10)
