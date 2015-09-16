# coding=utf-8
__author__ = 'titorx'

import socket
import threading


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

    request_queue_size = 5

    server_loop = True

    def __init__(self, server_address, request_handler_class):
        self.server_address = server_address
        self.request_handler_class = request_handler_class

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
        while self.server_loop:
            socket_request, client_address = self.get_request()
            self.handle_socket_request(socket_request, client_address)

    def handle_socket_request(self, socket_request, client_address):
        """ 处理请求 """
        self.request_handler_class(socket_request, client_address, self)

    def get_request(self):
        """ 获取连接 """
        return self.socket.accept()

    def server_stop(self):
        """ 停止服务 """
        self.server_loop = False

    def server_close(self):
        """ 关闭套接字 """
        self.server_stop()
        self.socket.close()


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

        self. request_handler_class = _TreadingHandler


class BaseSocketHandler:

    recv_num = 1024

    def __init__(self, socket_request, client_address, server):
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
            recv = self.socket_request.recv(self.recv_num)
            self.data += recv
            if len(recv) < self.recv_num:
                break

    def handle_socket_request(self):
        pass

    def finish(self):
        self.socket_request.close()

    def set_recv_num(self, num):
        self.recv_num = num
