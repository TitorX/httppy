from PyServer import HTTPServer
import thread


server_address = ('', 7777)


class Handler(HTTPServer.BaseHTTPHandler):
    def handle_request(self):
        self.http_response.body = 'hello world!'
        import json
        print('POST:' + json.dumps(self.http_request.POST, indent=4))
        print('GET:' + json.dumps(self.http_request.GET, indent=4))
        self.http_response.set_cookie('test', '123')


app = HTTPServer.BaseHTTPServer(server_address, Handler)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
