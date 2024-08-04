import gevent
from .data_types import GeckoDBString, GeckoDBNumber, GeckoDBNull, GeckoDBArray, GeckoDBDict

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

    def handle_get(self, key):
        """
        Retrieve the value associated with the given key.

        Args:
            key: The key to look up in the database.

        Returns:
            The value associated with the key, or None if the key doesn't exist.
        """
        return self.data.get(key, GeckoDBNull()).value

    def handle_set(self, key, value):
        """
        Set a key-value pair in the database.

        Args:
            key: The key to set.
            value: The value to associate with the key.

        Returns:
            'OK' to indicate successful operation.
        """
        # Determine the type of value and create appropriate GeckoDB object
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
        """
        Delete a key-value pair from the database.

        Args:
            key: The key to delete.

        Returns:
            'OK' if the key was deleted, 'NULL' if the key didn't exist.
        """
        if key in self.data:
            del self.data[key]
            return 'OK'
        return 'NULL'

    def handle_flush(self):
        """
        Clear all data from the database.

        Returns:
            'OK' to indicate successful operation.
        """
        self.data.clear()
        return 'OK'

    def handle_mget(self, keys):
        """
        Retrieve multiple values associated with the given keys.

        Args:
            keys: A list of keys to look up in the database.

        Returns:
            A list of values corresponding to the given keys.
        """
        return [self.handle_get(key) for key in keys]

    def handle_mset(self, pairs):
        """
        Set multiple key-value pairs in the database.

        Args:
            pairs: A dictionary of key-value pairs to set.

        Returns:
            'OK' to indicate successful operation.
        """
        for key, value in pairs.items():
            self.handle_set(key, value)
        return 'OK'