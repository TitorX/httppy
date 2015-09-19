__author__ = 'titorx'

from httppy import web
from httppy.template import render


class Index(web.RequestHandler):
    def handler(self):
        self.response.set_body('welcome httppy')


class UrlParam(web.RequestHandler):
    def handler(self):
        self.response.set_body(str(self.request.url_param))


class Template(web.RequestHandler):
    def handler(self):
        self.response.set_body(render.render('template/hello.html', {'hello': 'hello world'}))
