from exceptions import ExchangeError

class DatabaseUnavailableError(ExchangeError):
    def __init__(self, error: str=None):
        self.status_code = 503
        message = "База данных недоступна"
        if error is not None:
            message += f": {error}"
        super().__init__(message)

class StorageError(ExchangeError):
    def __init__(self, operation: str):
        self.status_code = 500
        message = f"Ошибка операции БД: {operation}"
        super().__init__(message)

class DatabaseOperationError(ExchangeError):
    def __init__(self):
        self.status_code = 500
        message = "Не удалось выполнить операцию"
        super().__init__(message)

class DataBaseValidatorError(ExchangeError):
    def __init__(self, missing_file: str = None):
        self.status_code = 500
        message = "Нет данных для валидатора"
        if missing_file is not None:
            message += f"отсутсвует файл: '{missing_file}'"
        super().__init__(message)