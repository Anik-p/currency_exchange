class ExchangeError(Exception):
    def __init__(self, message: str):
        self.status_code = 404
        super().__init__(message)