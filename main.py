# coding=utf-8
from httppy import httpserver
import thread, time

server_address = ('', 7777)


class Handler(httpserver.BaseHttpHandler):
    def handle_http_request(self):
        # global a
        # import time
        # time.sleep(10)
        self.http_response.body = 'hello world!'
        # print(self.http_request.ip)
        # import json
        # print('POST:' + json.dumps(self.http_request.POST, indent=4))
        # print('GET:' + json.dumps(self.http_request.GET, indent=4))
        # self.http_response.set_cookie('test1', '123', expires=10)
        # self.http_response.set_cookie('test2', '123', expires=10)


app = httpserver.BaseHttpServer(server_address, Handler)

thread.start_new_thread(app.server_start, ())

print('Server start')
print(server_address)
raw_input()
