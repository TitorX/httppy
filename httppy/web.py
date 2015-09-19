# coding=utf-8
__author__ = 'titorx'

import httpserver
import re


class Request(httpserver.HttpRequest):
    def __init__(self):
        httpserver.HttpRequest.__init__(self)
        self.url_param = {}


class Response(httpserver.HttpResponse):
    pass


class Response404(Response):
    def __init__(self):
        Response.__init__(self)
        self.set_status(404)


class WebHandler(httpserver.BaseHttpHandler):
    def __init__(self, socket_request, client_address, server, url_route):
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

    def set_response(self, content):
        self.response.set_body(content)

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
