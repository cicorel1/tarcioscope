from threading import Thread


class BroadcastThread(Thread):
    def __init__(self, picamera, websocket_server):
        super().__init__()
        self.picamera = picamera
        self.websocket_server = websocket_server


    def run(self):
        try:
            while not self.picamera.boutput is None:
                buf = self.picamera.boutput.converter.stdout.read1(32768)
                if buf:
                    self.websocket_server.send(buf, binary=True)
                elif self.picamera.boutput.converter.poll() is not None:
                    break
        except Exception as e:
            print(e)
        finally:
            self.picamera.stop_streaming()
