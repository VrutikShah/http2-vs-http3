import os
import ssl
from typing import cast

from aioquic.asyncio.protocol import QuicConnectionProtocol

# from utils import get_novel_name_server
import asyncio
from aioquic.quic import configuration
from aioquic.asyncio import QuicConnectionProtocol, connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived


class ImgClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = None

    async def send_data(self, file_name) -> None:
        data = file_name
        stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(stream_id, data.encode(), False)
        self.transmit()
        print(f"Sending data = {data} to server")


    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            if self.f is None:
                print("Opening for the first time")
                self.f = open("downloads/video.mp4", 'w+b')

            data = event.data
            self.f.write(data)


async def run(configuration: QuicConfiguration, host: str, port: int) -> None:
    print(f"Connecting to {host}:{port}")
    async with connect(
        host,
        port,
        configuration=configuration,
        create_protocol=ImgClient,
    ) as client:
        client = cast(ImgClient, client)
        # name of the file requested
        FileName = "video.mp4"
        await client.send_data(FileName)
        await client.wait_closed()


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    BUFFER_SIZE = 1024
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
class StreamingServerProtocol(QuicConnectionProtocol):
    def __init__(self, quic: connection.QuicConnection, stream_handler: Optional[QuicStreamHandler] = None):
        super().__init__(quic, stream_handler=stream_handler)

    def quic_event_received(self, event: events.QuicEvent) -> None:
        return super().quic_event_received(event)


def read_and_send(novel_no: str, connection, client_addr) -> None:
    
    function takes in novel number and
    socket connection to read the novel and send the data to client
    
    fname = get_novel_name_server(novel_no)
    print(fname)
    with open(fname, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            # print(len(data))
            if len(data) == 0:
                connection.sendto("F".encode(), client_addr)
                print("Sent Closing Packet. Closing Connection")
                break
            connection.sendto(data, client_addr)
    return


def create_server() -> None:
    
    * create server is the main function for program to behave as server.
    * Create socket -> Bind -> Listen -> Accept connection -> transfer file -> close
    cwd = os.getcwd()
    log_path = os.path.join(cwd, "logs")
    quic_logger = logger.QuicFileLogger(log_path)
    Qconf = configuration.QuicConfiguration(quic_logger=quic_logger, server_name="QUIC_SERVER")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Qserver.serve(HOST, PORT, configuration=Qconf))

    
    
    
    with so.socket(so.AF_INET, so.SOCK_DGRAM) as sock:
        sock.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR or so.SO_REUSEPORT, 1)
        sock.bind((HOST, PORT))
        recv_novel_no, client_addr = sock.recvfrom(BUFFER_SIZE)
        
        
        st = time.time()
        read_and_send(recv_novel_no.decode(), sock, client_addr)
        et = time.time()
        print(f"Time Taken - {(et-st):.4f}")



if __name__ == "__main__":
    create_server()
"""
