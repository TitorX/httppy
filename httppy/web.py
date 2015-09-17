# coding=utf-8
__author__ = 'titorx'

import httppy.httpserver as httpserver


class WebServer(httpserver.BaseHttpServer):

    class _Handler(httpserver.BaseHttpServer._Handler):
        def __init__(self, server, url_route):
            self.url_route = url_route
            httpserver.BaseHttpServer._Handler.__init__(self, server)

        def handle_request(self):
            self.handler(self.socket_request, self.client_address, self.server, self.url_route)

    def __init__(self, server_address, request_handler_class, url_route):
        self.url_route = url_route
        httpserver.BaseHttpServer.__init__(self, server_address, request_handler_class)

    def create_thread(self):
        return self._Handler(self, self.url_route)


class Request(httpserver.HttpRequest):
    pass


class Response(httpserver.HttpResponse):
    pass


class WebRequestHandler:

    def __init__(self):
        pass


class UrlRoute:

    """
    url路由
        负责将对应url请求分发给对应handler
    """

    def __init__(self, table):
        self.table = table

    def route(self, request=Request()):
        handler = self.table.get(request.url)
        if handler:
            response = handler(request)
        else:
            response = Response()
            response.set_status(404)
            response.body = 'not found'
        return response


class WebHandler(httpserver.BaseHttpHandler):
    def __init__(self, socket_request, client_address, server, url_route):
        self.url_route = url_route
        httpserver.BaseHttpHandler.__init__(self, socket_request, client_address, server)

    def handle_http_request(self):
        return self.url_route.route(self.http_request)
