# GeckoDB

GeckoDB is a lightweight, Redis-like key-value store implemented in Python using gevent for asynchronous I/O. It provides a simple yet powerful in-memory database with support for multiple data types and basic operations.


## Features

- Asynchronous I/O using gevent
- Support for multiple data types: strings, binary data, numbers, NULL, arrays, and dictionaries
- Basic operations: GET, SET, DELETE, FLUSH, MGET, MSET
- Simple network protocol for easy integration
- Extensible design for adding new features

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/geckodb.git
   cd geckodb
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage

There are multiple ways to run the GeckoDB server:

1. Using the installed command (after running `pip install -e .`):
   ```bash
   geckodb
   ```

2. As a Python module:
   ```bash
   python -m geckodb
   ```

3. Running the `__main__.py` file directly:
   ```bash
   python geckodb/__main__.py
   ```

The server will start on localhost:6380 by default.

To interact with the server, you can use a simple TCP client or implement your own client library. Here's an example using the `telnet` command:

```bash
$ telnet localhost 6380
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
SET mykey Hello,World!
OK
GET mykey
Hello,World!
```

## Supported Commands

- `GET <key>`: Retrieve the value of a key
- `SET <key> <value>`: Set the value of a key
- `DELETE <key>`: Delete a key
- `FLUSH`: Clear all keys from the database
- `MGET <key1> ... <keyn>`: Retrieve multiple values
- `MSET <key1> <value1> ... <keyn> <valuen>`: Set multiple key-value pairs

## Project Structure

```
geckodb/
│
├── geckodb/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   ├── data_types.py
│   └── protocol.py
│
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_data_types.py
│   └── test_protocol.py
│
├── README.md
├── requirements.txt
└── setup.py
```


## Running Tests

To run the tests, use the following command from the project root directory:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
