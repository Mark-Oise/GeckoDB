import json

def encode_message(message):
    """
    Encodes a message into a JSON string.

    Args:
        message: The message to be encoded.

    Returns:
        str: The JSON-encoded message.
    """
    return json.dumps(message)

def decode_message(raw_message):
    """
    Decodes a JSON string into a message.

    Args:
        raw_message: The JSON string to be decoded.

    Returns:
        dict: The decoded message.
    """
    return json.loads(raw_message)