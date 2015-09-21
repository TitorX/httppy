# coding=utf-8
__author__ = 'titorx'

import httpserver
import re


class Request(httpserver.HttpRequest):

    """
    httppy web 框架的基本请求类
    """

    def __init__(self):
        httpserver.HttpRequest.__init__(self)
        # 存储从url中解析得到的参数
        self.url_param = {}


class Response(httpserver.HttpResponse):

    """
    httppy web 框架的基本响应类
    """

    def __init__(self):
        httpserver.HttpResponse.__init__(self)
        # 默认返回内容的类型为html页面
        self.META['Content-Type'] = "text/html"

    def redirect(self, redirect_to):
        """
        将请求重定向到新的url
        :type redirect_to: str
        """
        self.set_status(302)
        self.set_header('Location', redirect_to)


class Response404(Response):

    """
    404响应类
    """

    def __init__(self):
        Response.__init__(self)
        self.set_status(404)


class WebHandler(httpserver.BaseHttpHandler):

    """
    httppy web 框架的handler
    """

    def __init__(self, socket_request, client_address, server, url_route):
        """
        :type socket_request: socket._socketobject
        :type client_address: (str, int)
        :type server: WebServer
        :type url_route: UrlRoute
        """
        self.url_route = url_route
        httpserver.BaseHttpHandler.__init__(self, socket_request, client_address, server)

    def handle_http_request(self):
        if not self.http_request.url.endswith('/'):
            self.http_request.url += '/'
        return self.url_route.route(self.http_request)


class WebServer(httpserver.BaseHttpServer):
    class _Handler(httpserver.BaseHttpServer._Handler):
        def __init__(self, server, url_route):
            self.url_route = url_route
            httpserver.BaseHttpServer._Handler.__init__(self, server)

        def handle_request(self):
            self.handler(self.socket_request, self.client_address, self.server, self.url_route)

    def __init__(self, server_address, url_route):
        """
        :type server_address: (str, int)
        :type url_route: UrlRoute
        """
        self.url_route = url_route
        httpserver.BaseHttpServer.__init__(self, server_address, WebHandler)

    def create_thread(self):
        return self._Handler(self, self.url_route)


class RequestHandler:

    """
    处理UrlRoute分发的请求
    """

    def __init__(self, request):
        """
        :type request: Request
        """
        self.request = request
        self.response = Response()

        self.setup()
        self.handler()
        self.finish()

    def setup(self):
        pass

    def handler(self):
        pass

    def finish(self):
        pass

    def get_response(self):
        return self.response


class UrlRoute:

    """
    url路由
        负责将对应url请求分发给对应handler
    """

    def __init__(self, route_table):
        """
        :type route_table: list
        """
        self.route_table = route_table
        self.convert_route_table()

    def convert_route_table(self):
        route_table = []
        for url, handler in self.route_table:
            route_table.append((re.compile(url), handler))
        self.route_table = route_table

    def route(self, request):
        """
        :type request: Request
        """
        response = None
        for url, handler in self.route_table:
            result = url.match(request.url)
            if result:
                request.url_param = result.groupdict()
                response = handler(request).get_response()
                break

        if not response:
            response = Response404()
        return response
