# coding=utf-8
__author__ = 'titorx'

import web
from multiprocessing import Process


class Manager:

    """
    一个对httppy库使用流程进行包装简化的管理框架类
    """

    def __init__(self, addresses, urls, **kwargs):
        """
        :type addresses: list
        :type urls: list
        """
        self.addresses = addresses
        self.urls = urls
        self.kwargs = kwargs
        self.servers = []
        self.url_route = None

        self.create_url_route()
        self.create_servers()

    def create_url_route(self):
        self.url_route = web.UrlRoute(self.urls)

    def create_servers(self):
        for address in self.addresses:
            app = web.WebServer(address, self.url_route)
            self.servers.append(Process(target=app.server_start))

    def setup(self):
        """ 对服务器进行初始化 """
        for server in self.servers:
            self.set_server(server, 'connect_timeout', self.kwargs.get('connect_timeout'))
            self.set_server(server, 'request_queue_size', self.kwargs.get('request_queue_size'))
            self.set_server(server, 'thread_pool_size', self.kwargs.get('thread_pool_size'))

    @staticmethod
    def set_server(server, key, value):
        """ 对服务器进行设置 """
        if value:
            setattr(server, key, value)

    def server_start(self):
        for server in self.servers:
            server.start()

        for server in self.servers:
            server.join()
