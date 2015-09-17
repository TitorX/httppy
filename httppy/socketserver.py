# coding=utf-8
__author__ = 'titorx'

import socket
import threading
from log import socket_server_log as log


class BaseTCPServer:

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
        get_request() → request_handler_class()

    """

    def __init__(self, server_address, request_handler_class):
        self.server_address = server_address
        self.request_handler_class = request_handler_class
        self.server_loop = True
        self.request_queue_size = 5
        self.connect_timeout = 5

        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_bind()
        self.server_listen()

    def server_bind(self):
        """ 套接字对象绑定到服务器端口 """
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_listen(self):
        """ 开始监听 """
        self.socket.listen(self.request_queue_size)

    def server_start(self):
        """ 开启服务 """
        log.info('Server start')
        while self.server_loop:
            socket_request, client_address = self.get_request()
            socket_request.settimeout(self.connect_timeout)
            self.handle_socket_request(socket_request, client_address)

    def handle_socket_request(self, socket_request, client_address):
        """ 处理请求 """
        self.request_handler_class(socket_request, client_address, self)

    def get_request(self):
        """ 获取连接 """
        return self.socket.accept()

    def server_stop(self):
        """ 停止服务 """
        s = socket.socket()
        s.connect(self.server_address)
        s.close()
        self.server_loop = False

    def server_close(self):
        """ 关闭服务 """
        self.server_stop()
        self.socket.close()

    def set_connect_timeout(self, timeout):
        self.connect_timeout = timeout


class ThreadingTCPServer(BaseTCPServer):

    """
    基于TCP套接字的多线程服务器类
    用于完成套接字层面的网络操作

    工作流程:
        bind()
          ↓
        listen()
          |
          |   loop  ←-------   ←
          ↓                    ↑
        get_request() → create_threading → request_handler_class()

    """

    def __init__(self, server_address, request_handler_class):
        BaseTCPServer.__init__(self, server_address, request_handler_class)

        class _TreadingHandler(threading.Thread):
            def __init__(self, socket_request, client_address, server):
                threading.Thread.__init__(self)
                self.socket_request = socket_request
                self.client_address = client_address
                self.server = server
                self.start()

            def run(self):
                request_handler_class(self.socket_request, self.client_address, self.server)

        self.request_handler_class = _TreadingHandler


class TreadPoolTCPServer(BaseTCPServer):

    """
    基于线程池的TCP服务器
    """

    def __init__(self, server_address, request_handler_class):
        BaseTCPServer.__init__(self, server_address, request_handler_class)
        self.thread_pool_size = 10
        self.thread_pool = []

        class _Handler(threading.Thread):
            def __init__(self, work_signal, server):
                threading.Thread.__init__(self)
                self.work_signal = work_signal
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
                    self.work_signal.wait()
                    try:
                        request_handler_class(self.socket_request, self.client_address, self.server)
                        self.socket_request = None
                        self.client_address = None
                    except Exception as e:
                        self.socket_request.close()
                        log.warn(e)
                    self.work_signal.clear()
                    # 工作完成后将自身添加回线程池中
                    self.server.thread_pool.append(self)

        for i in range(self.thread_pool_size):
            handler = _Handler(threading.Event(), self)
            self.thread_pool.append(handler)

    def handle_socket_request(self, socket_request, client_address):
        if self.thread_pool:
            handler = self.thread_pool.pop()
            handler.set_socket_request(socket_request, client_address)
            handler.work_signal.set()
        else:
            socket_request.close()

    def server_close(self):
        """ 关闭服务 """
        self.server_stop()
        self.socket.close()

    def set_thread_pool_size(self, size):
        """ 设置线程池大小 """
        self.thread_pool_size = size


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
