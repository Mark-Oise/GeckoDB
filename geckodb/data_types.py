class GeckoDBString:
    def __init__(self, value):
        """
        Initialize GeckoDBString with a string value.

        Args:
            value (str): The string value to store.
        """
        self.value = str(value)


class GeckoDBNumber:
    def __init__(self, value):
        """
        Initialize GeckoDBNumber with a float value.

        Args:
            value (float): The float value to store.
        """
        self.value = float(value)

class GeckoDBNull:
    def __init__(self, value):
        """
        Initialize GeckoDBNull with a None value.

        Args:
            value: None
        """
        self.value = None

class GeckoDBArray:
    def __init__(self, value):
        """
        Initialize GeckoDBArray with a list value.

        Args:
            value (list): The list value to store.
        """
        self.value = list(value)

class GeckoDBDictionary:
    def __init__(self, value):
        """
        Initialize GeckoDBDictionary with a dictionary value.

        Args:
            value (dict): The dictionary value to store.
        """
        self.value = dict(value)