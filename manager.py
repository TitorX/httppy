# coding=utf-8
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
        """
        对框架进行初始化
            可配置项
            connect_timeout 套接字连接超时时间
            request_queue_size 套接字listen监听队列
            thread_pool_size 线程池线程数
            404page 404页面
            500page 500页面
        """

        # 服务器设置
        def set_server(setup_server, key, value):
            """ 对服务器进行设置 """
            if value:
                setattr(setup_server, key, value)

        for server in self.servers:
            set_server(server, 'connect_timeout', self.kwargs.get('connect_timeout'))
            set_server(server, 'request_queue_size', self.kwargs.get('request_queue_size'))
            set_server(server, 'thread_pool_size', self.kwargs.get('thread_pool_size'))
        ####################################################################################
        # 404状态页
        page_404 = self.kwargs.get('404page')
        if page_404:
            web.UrlRoute.response404 = page_404
        ####################################################################################
        # 500状态页
        page_500 = self.kwargs.get('500page')
        if page_500:
            web.UrlRoute.response404 = page_500

    def server_start(self):
        for server in self.servers:
            server.start()

        for server in self.servers:
            server.join()
