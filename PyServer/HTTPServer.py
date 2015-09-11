__author__ = 'titorx'


from SocketServer import BaseRequestHandler, ThreadingTCPServer


class BaseHTTPServer(ThreadingTCPServer):
    pass


class HTTPRequest:
    def __init__(self):
        pass


class BaseHTTPHandler(BaseRequestHandler):
    def handle(self):
        print('Request from:' + str(self.client_address))
        print(self.data)
        self.request.sendall('hello socket')

