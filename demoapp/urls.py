# coding=utf-8
__author__ = 'titorx'

import handler


url = [
    (r'^/$', handler.Index),                                                        # 使用正则编写url
    (r'^/param/(?P<param1>[^/]+)/(?P<param2>[^/]+)/$', handler.UrlParam),           # 支持正则模块的分组
    (r'^/template/$', handler.Template),                                            # 模板系统使用例子
    (r'^/redirect/$', handler.Redirect),
]
