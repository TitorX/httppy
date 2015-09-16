__author__ = 'titorx'

import threading
import time

a = []

class Test(threading.Thread):
    def __init__(self, signal, name):
        threading.Thread.__init__(self)
        self.signal = signal
        self.name = name

    def run(self):
        global a
        a.append(1)
        print(self.name)

t = threading.Event()
t1 = Test(threading.Event(), 'test1')
t2 = Test(threading.Event(), 'test2')

t1.start()
t2.start()
for i in range(10):
    Test(threading.Event(), 'test1').start()

time.sleep(1)
print(len(a))
