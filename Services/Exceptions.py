class _OriginException(Exception):
    def __init__(self, message: str = None):
        if message is not None:
            raise Exception(message)


class NullException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)


class IDException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)


class NotAlterException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)


class ParcelaEmAbertoExcerption(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)


class ParcelasDefinidasException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)


class AutoValueException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)

class ProductException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)

class ClientException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)

class ContractException(_OriginException):
    def __init__(self, message: str = None):
        super().__init__(message)

class InstallmentDateException(_OriginException):
    def __init__(self, message: str = None):
        super.__init__(message)