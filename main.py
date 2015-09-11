from PyServer import SocketServer, HTTPServer
import thread
import threading


server_address = ('', 7777)


class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        print('Request from:' + str(self.client_address))
        print(self.data)
        self.request.send(str(threading.activeCount()))


class Handler1(HTTPServer.BaseHTTPHandler):
    pass


app = HTTPServer.BaseHTTPServer(server_address, Handler1)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
