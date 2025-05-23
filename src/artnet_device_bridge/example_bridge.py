from __future__ import annotations

import time

from pydantic import BaseModel
from stupidArtnet import StupidArtnet
from stupidArtnet import StupidArtnetServer


class ExampleBridge(BaseModel):
    # a Server object initializes with the following data
    # universe 			= DEFAULT 0
    # subnet   			= DEFAULT 0
    # net      			= DEFAULT 0
    # setSimplified     = DEFAULT True
    # callback_function = DEFAULT None

    recv_universe_id: int = 5
    send_universe_id: int = 6
    send_universe_ip: str = '192.168.120.45'

    _artnet_server: StupidArtnetServer = None
    _artnet_client: StupidArtnet = None

    def __init__(self):
        super().__init__()
        print('Hello from artnet-device-bridge!')

        # Create a server with the default port 6454
        self._artnet_server = StupidArtnetServer()
        self._artnet_client = StupidArtnet(
            self.send_universe_ip, self.send_universe_id, 512, 30, True, True,
        )

        self._recv_universe_listener = self._artnet_server.register_listener(
            self.recv_universe_id, callback_function=self.recv_callback,
        )

    def recv_callback(self, data, addr):
        # print('Received new addr \n', addr)
        # print('Received new data \n', data)

        # data[181-1] = data[181-1] + 2

        self._artnet_client.set(data)
        self._artnet_client.show()

    def main(self):
        try:
            while True:
                time.sleep(1)
        except Exception:
            if self._artnet_server is not None:
                del self._artnet_server


def main():
    example_bridge = ExampleBridge()
    example_bridge.main()
