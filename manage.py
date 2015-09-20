# coding=utf-8
__author__ = 'titorx'

import httppy


# 设置模板系统 ########################################
from httppy import template
template.render = template.get_template_render('template')
######################################################

# ####################################################
import urls

server_address = [
    ('', 7777),
    ('', 7778),
    ('', 7779)
]


manager = httppy.Manager(server_address, urls.urls)
manager.server_start()

######################################################
