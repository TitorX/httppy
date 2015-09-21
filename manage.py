# coding=utf-8
__author__ = 'titorx'

import httppy
import urls
from settings import conf, server_address

manager = httppy.Manager(server_address, urls.urls, **conf)
manager.server_start()
