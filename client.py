__author__ = 'titorx'
from socket import *
import threading
import time


address = ('', 7777)
ok = 0


def con(name):
    global ok
    s = socket()
    s.connect(address)
    s.send(name)
    # s.send('''GET /earth.jpg HTTP/1.1
    # Host: spellworks.net
    # User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
    # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    # Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    # Accept-Encoding: gzip, deflate
    # Connection: keep-alive
    # Range: bytes=401555-
    # If-Range: "55f13a45-6555a7"
    #
    # ''')
    max_len = 1024
    s.recv(max_len)
    s.close()
    ok += 1

threads = []
start = time.time()
for i in range(100):
    t = threading.Thread(target=con, args=('''GET /hello/world?123=123 HTTP/1.1
Host: localhost:7777
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cache-Control: max-age=0

''',))
    threads.append(t)
    t.start()

for i in threads:
    i.join()
end = time.time()
print('----------------')
print(end-start)
print(ok)
print('----------------')
