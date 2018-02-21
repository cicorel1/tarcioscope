from pprint import pprint
from struct import Struct

JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')

if __name__ == "__main__":
    from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

    from pi_camera_wrapper import PiCameraWrapper
    from broadcast_output import BroadcastOutput
    from broadcast_thread import BroadcastThread

    class PiCameraStreamApplication(WebSocketApplication):
        def on_open(self):
            jsmpeg_header = JSMPEG_HEADER.pack(JSMPEG_MAGIC, 640, 480)
            print("Connection opened. Sending header '%s'" % jsmpeg_header)
            self.ws.send(jsmpeg_header)

            try:
                picamera = PiCameraWrapper()
                output = BroadcastOutput(picamera)
                broadcast_thread = BroadcastThread(output.converter)
                picamera.start_streaming(output)

                broadcast_thread.start()

                # while True:
                #     picamera.camera.wait_recording(1)
            except KeyboardInterrupt:
                pass
            finally:
                print('Stopping recording')
                picamera.stop_streaming()
                print('Waiting for broadcast thread to finish')
                broadcast_thread.join()

        def on_close(self, reason):
            print(reason)

    websocket_server = WebSocketServer(('', 9000), Resource([
        ('/', PiCameraStreamApplication)
    ]))
    pprint(vars(websocket_server))
    websocket_server.serve_forever()

