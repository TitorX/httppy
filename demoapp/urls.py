# coding=utf-8
__author__ = 'titorx'

import handler


url = [
    (r'^/$', handler.Index),                              # 使用正则编写url
    (r'^/test/(?P<param>[^/]+)/$', handler.Param),        # 支持正则模块的分组
]


