import gevent


class GeckoDBServer:
    """
    A server class for GeckoDB.

    This class handles client connections and manages the database operations.
    """

    def __init__(self):
        """
        Initialize the GeckoDBServer.

        Creates an empty dictionary to store data.
        """
        self.data = {}  # Dictionary to store key-value pairs

    def handle_client(self, sock, address):
        """
        Handle a client connection.

        Args:
            sock (socket): The client socket object.
            address (tuple): The address of the client.

        This method creates a file-like object from the socket and enters a loop
        to continuously handle client requests.
        """
        fileobj = sock.makefile()  # Create a file-like object from the socket
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
        """
        Handle a command received from the client.

        Args:
            command (dict): The command received from the client.

        This method processes the command and performs the corresponding action.
        """
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