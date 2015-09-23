# coding=utf-8
__author__ = 'titorx'

from httppy import web
from httppy.template import render


class Index(web.RequestHandler):
    def handler(self):
        self.response.set_body(render.render('index.html', {}))


class UrlParam(web.RequestHandler):
    def handler(self):
        # 通过url正则获取到的参数可以通过 request.url_param 以字典形式取得
        self.response.set_body(str(self.request.url_param))


class Template(web.RequestHandler):
    def handler(self):
        # template中的render对象用于进行模板渲染
        # 模板系统使用jinja2
        # template中仅仅是对jinja2的包装
        import datetime
        self.response.set_body(render.render('template.html', {'time': '中文'}))


class Redirect(web.RequestHandler):
    def handler(self):
        self.response.redirect('/')
