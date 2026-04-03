class ExchangeError(Exception):
    status_code = 404
    def __init__(self, message: str):
        super().__init__(message)