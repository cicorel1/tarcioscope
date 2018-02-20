from threading import Thread

class BroadcastThread(Thread):
    def __init__(self, converter, websocket):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.websocket = websocket

    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read(512)
                if buf:
                    self.websocket.manager.broadcast(buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()
