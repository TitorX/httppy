# coding=utf-8
from httppy import web

server_address = ('', 7777)


def p(request):
    print(request.method)
    response = web.Response()
    response.body = 'hello world'
    return response

url_route = web.UrlRoute({'/': p})
app = web.WebServer(server_address, url_route)
app.server_start()
