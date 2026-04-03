from exceptions import ExchangeError

class DatabaseUnavailableError(ExchangeError):
    status_code = 503 
    def __init__(self, error: str=None):
        message = "База данных недоступна"
        if error is not None:
            message += f": {error}"
        super().__init__(message)

class ConfigurationError(ExchangeError):
    status_code = 500
    def __init__(self, config_key: str):
        message = f"Ошибка конфигурации: отсутствует или недопустима'{config_key}'"
        super().__init__(message)

class StorageError(ExchangeError):
    status_code = 500
    def __init__(self, operation: str):
        message = f"Ошибка операции БД: {operation}"
        super().__init__(message)