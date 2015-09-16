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
        while True:
            self.signal.wait()
            print(self.name)
            self.signal.clear()

t = threading.Event()
t1 = Test(threading.Event(), 'test1')

t1.start()

while True:
    a = raw_input()
    if a == '1':
        t1.signal.set()
