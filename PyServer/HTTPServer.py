# coding=utf-8
__author__ = 'titorx'


from SocketServer import BaseRequestHandler, ThreadingTCPServer


class BaseHTTPServer(ThreadingTCPServer):
    pass


class HTTPRequest:
    def __init__(self):
        self.header = ''
        self.body = ''
        self.ip = ''
        self.port = None


class BaseHTTPHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.http_request = HTTPRequest()
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.parse_http()
        print(self.http_request.header)

    def parse_http(self):
        # 获取客户端的ip port
        self.http_request.ip, self.http_request.port = self.client_address

        # 区分报文头部与主体
        header_len = self.data.find('\r\n\r\n')
        self.http_request.header = self.data[:header_len]
        self.http_request.body = self.data[header_len + 4:]

