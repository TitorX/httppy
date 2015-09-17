# coding=utf-8
__author__ = 'titorx'

import socket
import threading
import logging
import os


class BaseTCPServer(object):

    """
    基于TCP套接字的单线程服务器类
    用于完成套接字层面的网络操作

    工作流程:
        bind()
          ↓
        listen()
          |
          |   loop  ←-------      ←
          ↓                       ↑
        get_request() → handler()

    """

    def __init__(self, server_address, request_handler_class):
        self.logger = logging.getLogger(str(os.getpid()))
        self.server_address = server_address
        self.request_handler_class = request_handler_class
        self.server_loop = True
        self.request_queue_size = 5
        self.connect_timeout = 5

        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_bind()
        self.server_listen()

    def set_connect_timeout(self, timeout):
        """ 设置套接字连接超时时间 """
        self.connect_timeout = timeout

    def server_bind(self):
        """ 套接字对象绑定到服务器端口 """
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_listen(self):
        """ 开始监听 """
        self.socket.listen(self.request_queue_size)

    def server_start(self):
        """ 开启服务 """
        self.logger.info('Server start')
        self.logger.info('bind:' + str(self.server_address))
        while self.server_loop:
            socket_request, client_address = self.get_request()
            socket_request.settimeout(self.connect_timeout)
            self.handle_socket_request(socket_request, client_address)

    def get_request(self):
        """ 获取连接 """
        return self.socket.accept()

    def handle_socket_request(self, socket_request, client_address):
        """ 处理套接字请求 """
        self.request_handler_class(socket_request, client_address, self)

    def server_stop(self):
        """ 停止服务 """
        self.server_loop = False
        s = socket.socket()
        s.settimeout(0.1)
        s.connect(self.server_address)
        s.close()

    def server_close(self):
        """ 关闭服务 """
        self.server_stop()
        self.socket.close()


class TreadPoolTCPServer(BaseTCPServer):

    """
    基于线程池的TCP服务器
    """

    class _Handler(threading.Thread):
        def __init__(self, server):
            threading.Thread.__init__(self)
            self.handler = None
            self.work_signal = threading.Event()
            self.server = server
            self.socket_request = None
            self.client_address = None
            self.setDaemon(True)
            self.start()

        def set_socket_request(self, socket_request, client_address):
            self.socket_request = socket_request
            self.client_address = client_address

        def run(self):
            while True:
                # 等待工作开始的信号
                self.work_signal.wait()
                try:
                    self.handle_request()
                    self.socket_request = None
                    self.client_address = None
                except Exception as e:
                    self.socket_request.close()
                    self.server.logger.warn(e)
                self.work_signal.clear()
                # 工作完成后将自身添加回线程池中
                self.server.thread_pool.append(self)

        def set_request_handler(self, request_handler_class):
            """ 设置处理请求的类 """
            self.handler = request_handler_class

        def handle_request(self):
            self.handler(self.socket_request, self.client_address, self.server)

    def __init__(self, server_address, request_handler_class):
        BaseTCPServer.__init__(self, server_address, request_handler_class)
        # 线程池的最大线程数
        self.thread_pool_size = 10
        self.thread_pool = []

    def set_thread_pool_size(self, size):
        """ 设置线程池大小 """
        self.thread_pool_size = size

    def build_thread_pool(self):
        """ 创建线程池 """
        for i in range(self.thread_pool_size):
            handler = self.create_thread()
            handler.set_request_handler(self.request_handler_class)
            self.thread_pool.append(handler)

    def create_thread(self):
        """ 创建一条工作线程 """
        return self._Handler(self)

    def server_start(self):
        self.build_thread_pool()
        BaseTCPServer.server_start(self)

    def handle_socket_request(self, socket_request, client_address):
        """ 处理套接字请求 """
        if self.thread_pool:
            # 从线程池中取一条空闲线程
            handler = self.thread_pool.pop()
            handler.set_socket_request(socket_request, client_address)
            # 通知线程开始工作
            handler.work_signal.set()
        else:
            # 线程池中没有空闲线程 直接关闭套接字连接
            socket_request.close()


class BaseSocketHandler:

    def __init__(self, socket_request, client_address, server):
        self.recv_size = 1024
        self.data = ''
        self.socket_request = socket_request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.recv()
            self.handle_socket_request()
        finally:
            self.finish()

    def setup(self):
        pass

    def recv(self):
        while True:
            recv = self.socket_request.recv(self.recv_size)
            self.data += recv
            if len(recv) < self.recv_size:
                break

    def handle_socket_request(self):
        pass

    def finish(self):
        self.socket_request.close()

    def set_recv_num(self, size):
        self.recv_size = size
