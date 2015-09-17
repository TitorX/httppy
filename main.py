# coding=utf-8
# from httppy import log
from httppy import web
import thread, time, SimpleHTTPServer, sys

server_address = ('', 7777)


class Handler(web.WebHandler):
    pass
    # def handle_http_request(self):
        # import time
        # time.sleep(10)
        # self.http_response.body = 'hello world!'
        # print(self.http_request.ip)
        # print len(self.server.thread_pool)
        # import json
        # print('POST:' + json.dumps(self.http_request.POST, indent=4))
        # print('GET:' + json.dumps(self.http_request.GET, indent=4))
        # self.http_response.set_cookie('test1', '123', expires=10)
        # self.http_response.set_cookie('test2', '123', expires=10)


def p(request):
    print(request.method)
    response = web.Response()
    response.body = 'hello world'
    return response

url_route = web.UrlRoute({'/': p})
app = web.WebServer(server_address, Handler, url_route)
app.server_start()
