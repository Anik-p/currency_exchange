from exceptions import ExchangeError

class DatabaseUnavailableError(ExchangeError):
    status_code = 503 
    def __init__(self, error: str=None):
        message = "База данных недоступна"
        if error is not None:
            message += f": {error}"
        super().__init__(message)

class StorageError(ExchangeError):
    status_code = 500
    def __init__(self, operation: str):
        message = f"Ошибка операции БД: {operation}"
        super().__init__(message)

class DatabaseOperationError(ExchangeError):
    status_code = 500
    def __init__(self):
        message = f"Не удалось выполнить операцию"
        super().__init__(message)