# coding=utf-8
__author__ = 'titorx'

import web
from multiprocessing import Process


class Manager:

    """
    一个对httppy库使用流程进行包装简化的管理框架类
    """

    def __init__(self, addresses, urls):
        """
        :type addresses: list
        :type urls: list
        """
        self.addresses = addresses
        self.urls = urls
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

    def server_start(self):
        for server in self.servers:
            server.start()

        for server in self.servers:
            server.join()
