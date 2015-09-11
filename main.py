from PyServer import HTTPServer
import thread


server_address = ('', 7777)


class Handler(HTTPServer.BaseHTTPHandler):
    def handle(self):
        print('Request from:' + str(self.client_address))
        print(self.data)
        print(self.data.split('\r\n\r\n'))
        print(len(self.data.split('\r\n\r\n')))


app = HTTPServer.BaseHTTPServer(server_address, Handler)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
