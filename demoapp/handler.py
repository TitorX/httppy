__author__ = 'titorx'

from httppy import web


class Index(web.RequestHandler):
    def handler(self):
        self.response.body = 'welcome httppy'


class Param(web.RequestHandler):
    def handler(self):
        self.response.body = str(self.request.url_param)
