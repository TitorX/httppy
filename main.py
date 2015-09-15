from PyServer import HTTPServer
import threading

server_address = ('', 7777)


class Handler(HTTPServer.BaseHTTPHandler):
    def handle_request(self):
        self.http_response.body = 'hello world!'
        import json
        print('POST:' + json.dumps(self.http_request.POST, indent=4))
        print('GET:' + json.dumps(self.http_request.GET, indent=4))
        self.http_response.set_cookie('test1', '123')
        self.http_response.set_cookie('test', '12345')


app = HTTPServer.BaseHTTPServer(server_address, Handler)
t = threading.Thread(target=app.server_start)
t.start()
raw_input()
app.server_stop()
app.server_close()
