__author__ = 'titorx'


from httppy import web
import urls

server_address = ('', 7777)

url_route = web.UrlRoute(urls.urls)


app = web.WebServer(server_address, url_route)
app.server_start()
