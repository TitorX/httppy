# coding=utf-8
__author__ = 'titorx'

import httppy.httpserver as httpserver


class Request(httpserver.HttpRequest):
    pass


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


class WebRequestHandler:

    """
    处理UrlRoute分发的请求
    """

    def __init__(self):
        pass


class UrlRoute:

    """
    url路由
        负责将对应url请求分发给对应handler
    """

    def __init__(self, route_table):
        self.route_table = route_table

    def route(self, request=Request()):
        handler = self.route_table.get(request.url)
        if handler:
            response = handler(request)
        else:
            response = Response404()
        return response
