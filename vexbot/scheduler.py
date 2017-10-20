import os
from zmq.eventloop.zmqstream import ZMQStream

from vexmessage import decode_vex_message
from zmq.auth.ioloop import IOLoopAuthenticator 
from vexbot.util.get_certificate_filepath import get_certificate_filepath


class Scheduler:
    def __init__(self):
        # NOTE: This will probably go into the SocketFactory
        self.auth = IOLoopAuthenticator()
        self.auth.allow('127.0.0.1')
        certificate = get_certificate_filepath()
        public_key_location = os.path.join(certificate, 'public_keys')
        # self.auth.configure_cure(domain='*', public_key_location)
        self.auth.start()
        self._streams = []

    def register_socket(self, socket, loop, on_recv):
        stream = ZMQStream(socket, loop)
        stream.on_recv(on_recv)
        self._streams.append(stream)
