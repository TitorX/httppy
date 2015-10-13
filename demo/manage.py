# coding=utf-8
import sys
import os
sys.path.append(os.path.abspath('../..'))
import httppy
import urls
from settings import conf, server_address

manager = httppy.Manager(server_address, urls.urls, **conf)
manager.server_start()
