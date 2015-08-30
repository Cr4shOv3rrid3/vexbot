import os
import sys
import asyncio
from asyncio.streams import StreamWriter, FlowControlMixin

from adapters import Adapter

class Shell(Adapter):
    def __init__(self, bot=None):
        super(Shell, self).__init__()
        self._writer = None
        self._reader = None
        self.bot = bot

    def _stdio(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
            self._reader = asyncio.StreamReader()
            reader_protocol = asyncio.StreamReaderProtocol(self._reader)
            writer_transport, writer_protocol = yield from loop.connect_write_pipe(FlowControlMixin, os.fdopen(0, 'wb'))
            self._writer = StreamWriter(writer_transport, writer_protocol, None, loop)
            yield from loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)

    def send(self, message):
        if self._writer is not None:
            self._writer.write(message)

    @asyncio.coroutine
    def run(self, loop=None):
        # Initialzies the plugin
        yield from self._stdio()
        while True:
            self._writer.write(b'>>> ')
            line = yield from self._reader.readline()
            #print(line.decode('ascii'))
            # TODO: Fix/determine this api
            #bot.process_input(line)

if __name__ == '__main__':
    shell = Shell()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(shell.run(loop))
    finally:
        loop.close()