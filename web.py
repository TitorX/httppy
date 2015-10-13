# coding=utf-8
import httpserver
import re
import traceback


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
        self.handler()

    def handler(self):
        pass


class Response500(Response):

    """
    500响应类
    """

    def __init__(self):
        Response.__init__(self)
        self.set_status(500)
        self.handler()

    def handler(self):
        pass


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
        return self.url_route.route(self.http_request, self.server)


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

    def __init__(self, request, server):
        """
        :type request: Request
        :type server: WebServer
        """
        self.request = request
        self.server = server
        self.logger = self.server.logger
        self.response = Response()

        self.setup()
        self.handle()
        self.finish()

    def setup(self):
        pass

    def handle(self):
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

    response404 = Response404
    response500 = Response500

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

    def route(self, request, server):
        """
        :type request: Request
        :type server: WebServer
        """
        response = None
        for url, handler in self.route_table:
            result = url.match(request.url)
            if result:
                request.url_param = result.groupdict()
                try:
                    response = handler(request, server).get_response()
                except Exception as e:
                    # handler出错返回500错误
                    server.logger.warn('\n'.join([str(e), traceback.format_exc()]))
                    response = self.response500()
                break

        if not response:
            response = self.response404()
        return response
