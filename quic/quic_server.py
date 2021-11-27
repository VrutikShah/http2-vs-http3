import os
from typing import Dict, Optional
import asyncio
from aioquic.quic import configuration
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived
from aioquic.tls import SessionTicket

from utils import get_downloaded_fname_client

try:
    import uvloop
except ImportError:
    uvloop = None


class ImgServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = None
     
    def send_data(self, file_name) -> None:
        f = open(file_name, "rb")
        buffer_size = 2048
        data = f.read(buffer_size)
        stream_id = self._quic.get_next_available_stream_id()
        print("Sending data")
        while data:
            self._quic.send_stream_data(stream_id, data, False)
            self.transmit()
            data = f.read(buffer_size)
        print("Finished Sending")
        self.close()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            self.f = 1

            data = event.data
            print("Data", data)
            print("Writing data with stream id", event.stream_id)
            self.send_data("data/video.mp4")

class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: Dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> Optional[SessionTicket]:
        return self.tickets.pop(label, None)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    ROOT_PATH = os.getcwd()
    CERT_FOLDER = os.path.join(ROOT_PATH, "certs")
    CERT_FILE = os.path.join(CERT_FOLDER,"web-platform.test.pem")
    PK_FILE = os.path.join(CERT_FOLDER, "web-platform.test.key")
    LOG_PATH = os.path.join(ROOT_PATH, "logs")

    configuration = QuicConfiguration(
        alpn_protocols=["img_transfer"],
        is_client=False,
        max_datagram_frame_size=65536,
        quic_logger=None,
    )

    configuration.load_cert_chain(CERT_FILE, PK_FILE)

    ticket_store = SessionTicketStore()

    if uvloop is not None:
        uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        serve(
            HOST,
            PORT,
            configuration=configuration,
            create_protocol=ImgServerProtocol,
            session_ticket_fetcher=ticket_store.pop,
            session_ticket_handler=ticket_store.add
        )
    )
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
