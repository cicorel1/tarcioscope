class BroadcastThread
    def __init__(self, converter, ws_engine):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.ws_engine = ws_engine

    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read(512)
                if buf:
                    self.ws_engine.publish('websocket-broadcast', buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()
