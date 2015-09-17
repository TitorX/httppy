# coding=utf-8
__author__ = 'titorx'

from httppy import web


class Index(web.RequestHandler):
    def handler(self):
        self.response.body = 'welcome httppy'


class Param(web.RequestHandler):
    def handler(self):
        self.response.body = str(self.request.url_param)


url = {
    r'^/$': Index,                              # 使用正则编写url
    r'^/test/(?P<param>[^/]+)/$': Param,        # 支持正则模块的分组
}
# url的匹配完全使用re.match方法 调用groupdict方法将分组转化为字典传给Request.url_param

url_route = web.UrlRoute(url)

server_address = ('', 7777)
app = web.WebServer(server_address, url_route)
app.server_start()
