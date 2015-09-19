__author__ = 'titorx'

from httppy import web
from httppy.template import render


class Index(web.RequestHandler):
    def handler(self):
        self.set_response('welcome httppy')


class UrlParam(web.RequestHandler):
    def handler(self):
        self.set_response(str(self.request.url_param))


class Template(web.RequestHandler):
    def handler(self):
        self.set_response(render.render('template/hello.html', {'hello': 'hello world'}))
