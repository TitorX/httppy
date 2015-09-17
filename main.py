# coding=utf-8
from httppy import web

server_address = ('', 7777)


class C(web.RequestHandler):
    def handler(self):
        self.response.body = 'hello world!!'


url_route = web.UrlRoute({'/': C})
app = web.WebServer(server_address, url_route)
app.server_start()
