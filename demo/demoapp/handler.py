# coding=utf-8
from httppy import web
from httppy.template import render


class Index(web.RequestHandler):
    def handle(self):
        self.response.set_body(render('index.html', {}))


class UrlParam(web.RequestHandler):
    def handle(self):
        # 通过url正则获取到的参数可以通过 request.url_param 以字典形式取得
        self.response.set_body(str(self.request.url_param))


class Template(web.RequestHandler):
    def handle(self):
        # template中的render对象用于进行模板渲染
        # 模板系统使用jinja2
        # template中仅仅是对jinja2的包装
        import datetime

        self.response.set_body(render('template.html', {
            'time': datetime.datetime.now(),
            'cn': '欢迎',
        }))


class Redirect(web.RequestHandler):
    def handle(self):
        self.response.redirect('/')
