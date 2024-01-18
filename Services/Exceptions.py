class NullException(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)


class IDException(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)


class NotAlterException(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)


class ParcelaEmAbertoExcerption(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)


class ParcelasDefinidasException(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)
