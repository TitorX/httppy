from PyServer import HTTPServer
import thread


server_address = ('', 7777)


class Handler(HTTPServer.BaseHTTPHandler):
    pass


app = HTTPServer.BaseHTTPServer(server_address, Handler)
thread.start_new_thread(app.server_start, ())
raw_input()
app.server_close()
