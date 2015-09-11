from PyServer import SocketServer, SocketHandler
import thread
import threading


server_address = ('', 7777)


class Handler(SocketHandler.BaseRequestHandler):
    def handle(self):
        print('Request from:' + str(self.client_address))
        print(self.data)
        self.request.send(str(threading.activeCount()))

app = SocketServer.ThreadingTCPServer(server_address, Handler)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
