# coding=utf-8
__author__ = 'titorx'


from SocketServer import BaseRequestHandler, ThreadingTCPServer
import urllib
import StringIO


class BaseHTTPServer(ThreadingTCPServer):
    pass


class HTTPRequest:

    """
    http请求对象 每个浏览器发送到服务器的请求对应生成一个HTTPRequest对象

    header 原始报文首部
    body 原始报文主体
    ip port 发起请求者的ip port
    http_version 请求使用的http版本
    method 请求方法

    url 请求的url
    get_string 请求的get部分字符串
        url?get_string 原始的完整请求url

    META 字典(dict)形式的解析后的报文首部
        首部字段的key全部转化为大写(.upper())
        如:
            self.META = {
                'CONNECTION': 'keep-alive'
            }

    GET 字典(dict)形式的解析后的get参数
    COOKIE 字典(dict)形式的解析后的cookie参数
    POST 字典(dict)形式的解析后的post参数

    FILE 字典(dict)形式的解析后的上传文件
        self.FILE = {
            'file1': {
                'CONTENT-TYPE': 'image/jpeg',
                'filename': 'test.jpg',
                'content': StringIO.StringIO(文件二进制)
            }
        }

    """

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

    """
    对http请求的响应对象

    """

    class _Cookie:

        """
        用于cookie处理
        """

        def __init__(self):
            self.COOKIE = {}
            self.domain = None
            self.expires = None
            self.path = None

        def set_cookie(self, key, value, expires, path, domain):
            """
            设置cookie 最后一次设置的path domain生效
            """
            self.domain = domain
            self.path = path

            self.COOKIE[key] = '='.join([key, value])
            if expires:
                self.COOKIE[key] += ', expires=%s;' % 'time'
            else:
                self.COOKIE[key] += ';'

        def get_set_cookie_meta(self):
            """
            返回 (Set-Cookie, xxx) 形式的元组,用于后续响应头部信息
            """
            if self.COOKIE:
                set_cookie = [i for i in self.COOKIE.values()]
                if self.path:
                    set_cookie.append('path=%s;' % self.path)
                if self.domain:
                    set_cookie.append('domain=%s;' % self.domain)

                set_cookie_string = ' '.join(set_cookie)
                return 'Set-Cookie', set_cookie_string
            else:
                return None

    def __init__(self):
        self.http_version = 'HTTP/1.1'
        self.status = '200'
        self.header = ''
        self.body = ''
        self.META = {
            'Server': 'PyHTTPServer/0.1'
        }
        self.cookie = self._Cookie()

    def set_header(self, key, value):
        self.META[key] = value

    def set_cookie(self, key, value, expires=None, path=None, domain=None):
        self.cookie.set_cookie(key, value, expires, path, domain)

    def make_header(self):
        set_cookie_meta = self.cookie.get_set_cookie_meta()
        if set_cookie_meta:
            self.META[set_cookie_meta[0]] = set_cookie_meta[1]

        self.header = '\r\n'.join([key + ': ' + value for key, value in self.META.iteritems()])

    def get_response(self):
        """ 该方法返回一个字符串形式的http响应 """
        self.make_header()

        response_line = ' '.join([self.http_version, self.status])
        response = response_line + '\r\n' + self.header + '\r\n\r\n' + self.body
        return response


class BaseHTTPHandler(BaseRequestHandler):

    """
    进行HTTP协议的解析
    self.http_request 请求对象
    self.http_response 响应对象
    """

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
        """ 解析http """
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
        """ 解析请求行以及请求头部 """
        header_lines = self.http_request.header.splitlines()
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
        """ 解析get参数 """
        if self.http_request.get_string:
            for get_string in self.http_request.get_string.split('&'):
                get = get_string.split('=')
                # 当出现get参数没写完整的情况时 如:?a&b=1 添加一个''使不完整的参数赋值为''
                get.append('')
                self.http_request.GET[get[0]] = get[1]

    def parse_cookie(self):
        """ 解析cookie参数 """
        cookie_string = self.http_request.META.get('COOKIE', '')
        if cookie_string:
            for cookies in cookie_string.split('; '):
                cookie = cookies.split('=')
                self.http_request.COOKIE[cookie[0]] = cookie[1]

    def parse_post(self):
        """ 解析post得到的参数以及文件 """
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
                        'filename': chunk_meta['filename'],
                        'content': StringIO.StringIO(chunk_body)
                    }

        else:
            body = urllib.unquote(self.http_request.body[:content_length])
            for posts in body.split('&'):
                post = posts.split('=')
                self.http_request.POST[post[0]] = post[1]

    def send_response(self):
        self.socket_request.sendall(self.http_response.get_response())
