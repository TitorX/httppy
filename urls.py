__author__ = 'titorx'

import demoapp.urls
from httppy.statichandler import static_handler
import os

urls = [
    (r'/static/(?P<path>.*)$', static_handler(os.path.join(os.getcwd(), 'static')))
]

urls += demoapp.urls.url

