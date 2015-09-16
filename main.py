from httppy import httpserver
import threading

server_address = ('', 7777)


class Handler(httpserver.BaseHttpHandler):
    def handle_http_request(self):
        self.http_response.body = 'hello world!'
        import json
        print('POST:' + json.dumps(self.http_request.POST, indent=4))
        print('GET:' + json.dumps(self.http_request.GET, indent=4))
        self.http_response.set_cookie('test1', '123', expires=10)
        self.http_response.set_cookie('test2', '123', expires=10)


app = httpserver.BaseHttpServer(server_address, Handler)
t = threading.Thread(target=app.server_start)
t.start()
t.join()
