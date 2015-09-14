from PyServer import HTTPServer
import thread


server_address = ('', 7777)


class Handler(HTTPServer.BaseHTTPHandler):
    def handle_request(self):
        self.http_response.body = 'hello world!'
        import json
        print(json.dumps(self.http_request.POST, indent=4))


app = HTTPServer.BaseHTTPServer(server_address, Handler)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
