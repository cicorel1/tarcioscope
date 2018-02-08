import asyncio


from pyramid.view import view_config
from aiopyramid.websocket.config import WebsocketMapper
from broadcast_output import BroadcastOutput


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return {'project': 'Tarcioscope'}

@view_config(route_name='video', mapper=WebsocketMapper)
@asyncio.coroutine
def socket(ws):
    while True:
        camera.wait_recording(1)
