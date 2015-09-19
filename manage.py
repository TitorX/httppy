# coding=utf-8
__author__ = 'titorx'


# 设置模板系统 ########################################
from httppy import template
template.render = template.get_template_render('test')
######################################################


from httppy import web
import urls

server_address = ('', 7777)

url_route = web.UrlRoute(urls.urls)


app = web.WebServer(server_address, url_route)
app.server_start()
