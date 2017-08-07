import threading
import time

flag=True

def worker():
    global flag
    while flag:
        print(threading.current_thread().getName(), 'Starting')
        time.sleep(0.2)


w = threading.Thread(name='worker', target=worker)

w.start()
time.sleep(4)
flag=False
