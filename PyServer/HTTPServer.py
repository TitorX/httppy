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
        self.http_version = ''


class HTTPResponse:
    def __init__(self):
        self.status = ''

    def response(self):
        return '''HTTP/1.1 200 ok
Content-type: text/html

<html>
<body>
<h1>hello world</h1>
</body>
</html>
'''


class BaseHTTPHandler(BaseRequestHandler):
    def __init__(self, socket_request, client_address, server):
        self.http_request = HTTPRequest()
        self.http_response = HTTPResponse()
        BaseRequestHandler.__init__(self, socket_request, client_address, server)

    def handle(self):
        self.parse_http()
        print(self.http_request.header)
        self.send_response()

    def parse_http(self):
        # 获取客户端的ip port
        self.http_request.ip, self.http_request.port = self.client_address

        # 区分报文头部与主体
        header_len = self.data.find('\r\n\r\n')
        self.http_request.header = self.data[:header_len]
        self.http_request.body = self.data[header_len + 4:]

    def send_response(self):
        self.socket_request.sendall(self.http_response.response())
