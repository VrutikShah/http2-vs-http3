# https://github.com/aiortc/aioquic repo examples folder
# demo application for http3_server.py
#

import datetime
import os
from urllib.parse import urlencode
import requests

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.types import Receive, Scope, Send

ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.environ.get("STATIC_ROOT", os.path.join(ROOT, "htdocs"))
STATIC_URL = "/"
LOGS_PATH = os.path.join(STATIC_ROOT, "logs")
QVIS_URL = "https://qvis.quictools.info/"

templates = Jinja2Templates(directory=os.path.join(ROOT, "templates"))


async def echo(request):
    """
    HTTP echo endpoint.
    """
    content = await request.body()
    media_type = request.headers.get("content-type")
    return Response(content, media_type=media_type)


async def logs(request):
    """
    Browsable list of QLOG files.
    """
    logs = []
    for name in os.listdir(LOGS_PATH):
        if name.endswith(".qlog"):
            s = os.stat(os.path.join(LOGS_PATH, name))
            file_url = "https://" + request.headers["host"] + "/logs/" + name
            logs.append(
                {
                    "date": datetime.datetime.utcfromtimestamp(s.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "file_url": file_url,
                    "name": name[:-5],
                    "qvis_url": QVIS_URL
                    + "?"
                    + urlencode({"file": file_url})
                    + "#/sequence",
                    "size": s.st_size,
                }
            )
    return templates.TemplateResponse(
        "logs.html",
        {
            "logs": sorted(logs, key=lambda x: x["date"], reverse=True),
            "request": request,
        },
    )


# async def send_video(request):
#     """
#     send the video file
    
#     """
#     VIDEO_FILE = "data/output3.mpd"
#     files = {'file': open(VIDEO_FILE, 'rb')}
#     with requests.Session() as session:
#         response = session.post(request, files=files, stream=True)
#     return response


# async def ws(websocket):
#     """
#     WebSocket echo endpoint.
#     """
#     if "chat" in websocket.scope["subprotocols"]:
#         subprotocol = "chat"
#     else:
#         subprotocol = None
#     await websocket.accept(subprotocol=subprotocol)

#     try:
#         while True:
#             message = await websocket.receive_text()
#             await websocket.send_text(message)
#     except WebSocketDisconnect:
#         pass


# async def wt(scope: Scope, receive: Receive, send: Send) -> None:
#     """
#     WebTransport echo endpoint.
#     """
#     # accept connection
#     message = await receive()
#     assert message["type"] == "webtransport.connect"
#     await send({"type": "webtransport.accept"})

#     # echo back received data
#     while True:
#         message = await receive()
#         if message["type"] == "webtransport.datagram.receive":
#             await send(
#                 {
#                     "data": message["data"],
#                     "type": "webtransport.datagram.send",
#                 }
#             )
#         elif message["type"] == "webtransport.stream.receive":
#             await send(
#                 {
#                     "data": message["data"],
#                     "stream": message["stream"],
#                     "type": "webtransport.stream.send",
#                 }
#             )


starlette = Starlette(
    routes=[
        Route("/echo", echo, methods=["POST"]),
        # WebSocketRoute("/ws", ws),
    ]
)


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    # if scope["type"] == "webtransport" and scope["path"] == "/wt":
    #     await wt(scope, receive, send)
    # else:
    await starlette(scope, receive, send)