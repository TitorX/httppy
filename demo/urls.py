# coding=utf-8
import demoapp.urls
from httppy.statichandler import static_handler
import os

urls = [
    (r'^/static/(?P<path>.*)$', static_handler(os.path.join(os.getcwd(), 'httppy/demo/static'))),     # 处理静态文件
]

urls += demoapp.urls.url
