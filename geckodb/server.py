import gevent
from gevent import socket
from gevent.server import StreamServer
from geckodb.data_types import GeckoDBString, GeckoDBNumber, GeckoDBNull, GeckoDBArray, GeckoDBDictionary
from geckodb.protocol import encode_message, decode_message

class GeckoDBServer:
    """
    A server class for GeckoDB that handles client connections and manages database operations.
    """

    def __init__(self):
        self.data = {}

    def handle_client(self, sock, address):
        fileobj = sock.makefile()
        while True:
            line = fileobj.readline()
            if not line:
                break
            try:
                command = decode_message(line.strip())
                result = self.handle_command(command)
                fileobj.write(encode_message(result) + '\n')
                fileobj.flush()
            except Exception as e:
                fileobj.write(encode_message(f"ERROR: {str(e)}") + '\n')
                fileobj.flush()

    def handle_command(self, command):
        cmd = command['command'].upper()
        if cmd == 'GET':
            return self.handle_get(command['key'])
        elif cmd == 'SET':
            return self.handle_set(command['key'], command['value'])
        elif cmd == 'DELETE':
            return self.handle_delete(command['key'])
        elif cmd == 'FLUSH':
            return self.handle_flush()
        elif cmd == 'MGET':
            return self.handle_mget(command['keys'])
        elif cmd == 'MSET':
            return self.handle_mset(command['pairs'])
        else:
            raise ValueError(f'Unknown command: {cmd}')

    def handle_get(self, key):
        return self.data.get(key, GeckoDBNull()).value

    def handle_set(self, key, value):
        if isinstance(value, (int, float)):
            self.data[key] = GeckoDBNumber(value)
        elif isinstance(value, list):
            self.data[key] = GeckoDBArray(value)
        elif isinstance(value, dict):
            self.data[key] = GeckoDBDict(value)
        elif value is None:
            self.data[key] = GeckoDBNull()
        else:
            self.data[key] = GeckoDBString(value)
        return 'OK'

    def handle_delete(self, key):
        if key in self.data:
            del self.data[key]
            return 'OK'
        return 'NULL'

    def handle_flush(self):
        self.data.clear()
        return 'OK'

    def handle_mget(self, keys):
        return [self.handle_get(key) for key in keys]

    def handle_mset(self, pairs):
        for key, value in pairs.items():
            self.handle_set(key, value)
        return 'OK'


def main():
    server = GeckoDBServer()
    stream_server = StreamServer(('localhost', 6380), server.handle_client)
    print('GeckoDB server started on localhost:6380')
    stream_server.serve_forever()


if __name__ == "__main__":
    main()
