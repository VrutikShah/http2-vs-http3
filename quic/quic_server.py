import os
import math
from typing import Dict, Optional
import asyncio
from aioquic.quic import configuration
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived
from aioquic.tls import SessionTicket

try:
    import uvloop
except ImportError:
    uvloop = None


class StreamingServer(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = None
        self._ack_waiter: Optional[asyncio.Future[None]] = None

     
    def send_data(self, file_name) -> None:
        f = open(file_name, "rb")
        buffer_size = 1048576
        data = f.read(buffer_size)
        stream_id = self._quic.get_next_available_stream_id()
        stream_end = False
        print("Sending data")
        num_packets = math.ceil(os.path.getsize(file_name)/buffer_size)
        print("Size is", os.path.getsize(file_name),"buffer is", buffer_size, "num_packets=", num_packets)
        counter = 1
        while (data):
            print(f"Sending {counter} packet")
            if counter == num_packets:
                print("Set stream end to True!")
                stream_end = True
            self._quic.send_stream_data(stream_id, data, stream_end)
            self.transmit()
            data = f.read(buffer_size)
            counter += 1

        waiter = self._loop.create_future()
        self._ack_waiter = waiter

        # self.close()
        return asyncio.shield(waiter)
            
    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            response = event.data
            print(response.decode())
            # waiter = self._ack_waiter
            # self._ack_waiter = None
            self.send_data("data/video.mp4")
            # waiter.set_result(None)

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
    HOST = "10.7.19.226"
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
            create_protocol=StreamingServer,
            session_ticket_fetcher=ticket_store.pop,
            session_ticket_handler=ticket_store.add
        )
    )
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
