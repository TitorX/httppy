# coding=utf-8
__author__ = 'titorx'


from SocketServer import BaseRequestHandler, ThreadingTCPServer
import urllib
import StringIO


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
        if self.http_request.method == 'POST':
            self.parse_post()

    def parse_header(self):
        header_lines = self.http_request.header.splitlines()
        print(self.http_request.header)
        # 解析请求行
        request_line = header_lines[0]
        request_line = request_line.split()
        self.http_request.method = request_line[0]

        request = request_line[1].split('?')
        # 当url中没有?时 如:/index/index 添加一个''使get_string为''
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
                # 当出现get参数没写完整的情况时 如:?a&b=1 添加一个''使不完整的参数赋值为''
                get.append('')
                self.http_request.GET[get[0]] = get[1]

    def parse_cookie(self):
        cookie_string = self.http_request.META.get('COOKIE', '')
        if cookie_string:
            for cookies in cookie_string.split('; '):
                cookie = cookies.split('=')
                self.http_request.COOKIE[cookie[0]] = cookie[1]

    def parse_post(self):
        content_type = self.http_request.META.get('CONTENT-TYPE', '')
        content_length = int(self.http_request.META.get('CONTENT-LENGTH', -1)) + 1

        if 'multipart/form-data' in content_type:
            boundary = content_type.split('; ')[1].split('=')[1]
            chunks = self.http_request.body.split('--' + boundary)[1:-1]
            for chunk in chunks:
                chunk_header_len = chunk.find('\r\n\r\n')
                chunk_header = chunk[:chunk_header_len]
                # [:-2] 截取掉末尾的\r\n
                chunk_body = chunk[chunk_header_len + 4:-2]
                chunk_meta = {}

                # 解析chunk header
                for header_line in chunk_header.splitlines():
                    if header_line:
                        header_line = header_line.split('; ')

                        meta = header_line[0].split(': ')
                        chunk_meta[meta[0].upper()] = meta[1]

                        if len(header_line) > 1:
                            for header in header_line[1:]:
                                meta = header.split('=')
                                chunk_meta[meta[0]] = meta[1].strip('\"')

                # 解析 chunk body
                if not chunk_meta.get('CONTENT-TYPE', ''):
                    self.http_request.POST[chunk_meta['name']] = chunk_body
                else:
                    self.http_request.FILE[chunk_meta['name']] = {
                        'CONTENT-TYPE': chunk_meta['CONTENT-TYPE'],
                        'filename': StringIO.StringIO(chunk_meta['filename']),
                        'content': chunk_body
                    }

        else:
            body = urllib.unquote(self.http_request.body[:content_length])
            for posts in body.split('&'):
                post = posts.split('=')
                self.http_request.POST[post[0]] = post[1]

    def send_response(self):
        self.socket_request.sendall(self.http_response.response())
