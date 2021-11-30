import os
import ssl
from typing import Optional, cast

from aioquic.asyncio.protocol import QuicConnectionProtocol

import asyncio
from aioquic.quic import configuration
from aioquic.asyncio import QuicConnectionProtocol, connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived


class StreamingClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = None
        self._ack_waiter: Optional[asyncio.Future[None]] = None

    async def send_data(self, file_name) -> None:
        data = file_name.encode()
        stream_id = self._quic.get_next_available_stream_id()
        stream_end = True
        self._quic.send_stream_data(stream_id, data, stream_end)
        self.transmit()
        print(f"Sent {data} to server")

        waiter = self._loop.create_future()
        self._ack_waiter = waiter

        return await asyncio.shield(waiter)

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            if self.f is None:
                print("Opening for the first time")
                self.f = open("downloads/video.mp4", 'w+b')
            data = event.data
            self.f.write(data)
            if event.end_stream:
                self.f.close()
                print("Finished writing to file")
                return

async def run(configuration: QuicConfiguration, host: str, port: int) -> None:
    print(f"Connecting to {host}:{port}")
    async with connect(
        host,
        port,
        configuration=configuration,
        create_protocol=StreamingClient,
    ) as client:
        client = cast(StreamingClient, client)
        # name of the file requested
        FileName = "video.mp4"
        await client.send_data(FileName)
        await client.wait_closed()


if __name__ == "__main__":
    HOST = "10.7.19.226"
    PORT = 12345
    BUFFER_SIZE = 2048
    ROOT_PATH = os.getcwd()
    CERT_FOLDER = os.path.join(ROOT_PATH, "certs")
    CA_CERT = os.path.join(CERT_FOLDER, "cacert.pem")
    CA_PK = os.path.join(CERT_FOLDER, "cacert.key")

    configuration = QuicConfiguration(
        alpn_protocols=["img_transfer"], is_client=True, max_datagram_frame_size=65536
    )
    configuration.load_verify_locations(CA_CERT)
    configuration.verify_mode = ssl.CERT_NONE
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(configuration=configuration, host=HOST, port=PORT))


"""
class StreamingClient(QuicConnectionProtocol):
    def __init__(self, quic: connection.QuicConnection, stream_handler: Optional[QuicStreamHandler] = None):
        super().__init__(quic, stream_handler=stream_handler)

    def quic_event_received(self, event: events.QuicEvent) -> None:
        return super().quic_event_received(event)
"""