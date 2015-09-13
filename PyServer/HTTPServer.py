# coding=utf-8
__author__ = 'titorx'


from SocketServer import BaseRequestHandler, ThreadingTCPServer
import urllib


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
        self.GET = {}
        self.COOKIE = {}
        self.POST = {}
        self.FILE = {}


class HTTPResponse:
    def __init__(self):
        self.status = ''

    def response(self):
        return '''HTTP/1.1 200 ok
Set-Cookie: a=中文Cookie; path=/;

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
        self.parse_get()
        self.parse_cookie()
        self.parse_post()

    def parse_header(self):
        header_lines = self.http_request.header.splitlines()
        print(self.http_request.header)
        # 解析请求行
        request_line = header_lines[0]
        request_line = request_line.split()
        self.http_request.method = request_line[0]

        request = request_line[1].split('?')
        request.append('')
        self.http_request.url, self.http_request.get_string = request[0], urllib.unquote(request[1])

        self.http_request.http_version = request_line[2]

        # 解析报文首部
        for one_line in header_lines[1:]:
            meta = one_line.split(': ')
            self.http_request.META[meta[0].upper()] = meta[1]

    def parse_get(self):
        if self.http_request.get_string:
            for get_string in self.http_request.get_string.split('&'):
                get = get_string.split('=')
                get.append('')
                self.http_request.GET[get[0]] = get[1]

    def parse_cookie(self):
        cookie_string = self.http_request.META.get('COOKIE', '')
        if cookie_string:
            for cookies in cookie_string.split('; '):
                cookie = cookies.split('=')
                self.http_request.COOKIE[cookie[0]] = cookie[1]

    def parse_post(self):
        pass

    def send_response(self):
        self.socket_request.sendall(self.http_response.response())
