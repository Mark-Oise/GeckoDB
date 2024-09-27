class GeckoDBString:
    def __init__(self, value):
        self.value = str(value)


class GeckoDBNumber:
    def __init__(self, value):
        self.value = float(value)


class GeckoDBNull:
    def __init__(self, value):
        self.value = None


class GeckoDBArray:
    def __init__(self, value):
        self.value = list(value)


class GeckoDBDictionary:
    def __init__(self, value):
        self.value = dict(value)
