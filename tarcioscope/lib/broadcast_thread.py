from threading import Thread


class BroadcastThread(Thread):
    def __init__(self, picamera, websocket_server):
        super().__init__()
        self.picamera = picamera
        self.websocket_server = websocket_server


    def run(self):
        try:
            while not self.websocket_server.terminated:
                buf = self.picamera.output.converter.stdout.read1(32768)
                if buf:
                    self.websocket_server.send(buf, binary=True)
                elif self.picamera.output.converter.poll() is not None:
                    break
        finally:
            self.picamera.stop_streaming()
