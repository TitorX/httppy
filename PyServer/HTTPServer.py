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
        self.method = ''
        self.url = ''
        self.get_string = ''
        self.META = {}
        self.FILE = {}


class HTTPResponse:
    def __init__(self):
        self.status = ''

    def response(self):
        return '''HTTP/1.1 200 ok

<html>
<head>
<meta charset="UTF-8">
<title>欢迎</title>
</head>
<body>
<h1>中文</h1>
<h1>にほんご</h1>
<h1>한국어</h1>
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
        self.handle_request()
        self.send_response()

    def handle_request(self):
        """ 由用户进行重载 对http request进行处理 """
        pass

    def parse_http(self):
        # 获取客户端的ip port
        self.http_request.ip, self.http_request.port = self.client_address

        # 区分报文头部与主体
        header_len = self.data.find('\r\n\r\n')
        self.http_request.header = self.data[:header_len]
        self.http_request.body = self.data[header_len + 4:]

        self.parse_header()

    def parse_header(self):
        header_lines = self.http_request.header.splitlines()

        # 解析请求行
        request_line = header_lines[0]
        request_line = request_line.split()
        self.http_request.method = request_line[0]
        if '?' in request_line:
            self.http_request.url, self.http_request.get_string = request_line[1].split('?')
        else:
            self.http_request.url = request_line[1]
            self.http_request.get_string = ''
        self.http_request.http_version = request_line[2]

        # 解析报文首部
        for one_line in header_lines[1:]:
            meta = one_line.split(': ')
            self.http_request.META[meta[0].upper()] = meta[1]

    def send_response(self):
        self.socket_request.sendall(self.http_response.response())
