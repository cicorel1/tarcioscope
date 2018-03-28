import socketserver
from http import server

from lib import streaming_handler


HOST = '0.0.0.0'
PORT = 8000

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    server = StreamingServer((HOST, PORT), streaming_handler.StreamingHandler)
    server.serve_forever()
