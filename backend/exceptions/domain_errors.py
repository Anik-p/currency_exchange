from exceptions import ExchangeError

class IncorrectCurrencyData(ExchangeError):
    def __init__(self):
        self.status_code = 400
        message = "Обязательное поле формы не заполнено"
        super().__init__(message)

class IncorrectInputCodeCurrency(ExchangeError):
    def __init__(self, params: str=None):
        self.status_code = 400
        message = "Данный ввод валюты не корректен"
        if params is not None:
            message += f": {params}"
        super().__init__(message)

class CurrenciesNotFoundError(ExchangeError):
    def __init__(self):
        self.status_code = 400
        message = "База данных не содержит данных о валюте"
        super().__init__(message) 

class InvalidCurrencyError(ExchangeError):
    def __init__(self, base: str):
        self.status_code = 400
        message = f"Неизвестный код валюты '{base}'"
        super().__init__(message)

class InvalidAmountError(ExchangeError):
    def __init__(self):
        self.status_code = 400
        message = "Ошибка при расчете обменного курса"
        super().__init__(message)   

class CurrencyPairInputError(ExchangeError):
    def __init__(self):
        self.status_code = 400
        message = (f"В адресе отсутствуют коды валютной пары")
        super().__init__(message)

class InvalidRateError(ExchangeError):
    def __init__(self, base: str, target: str):
        self.status_code = 400
        message = f"Невозможно рассчитать обменный курс для '{base}' и '{target}'"
        super().__init__(message)

class InvalidCrossRateError(ExchangeError):
    def __init__(self):
        self.status_code = 403
        message = f"Невозможно рассчитать кросс курс, поскольку одна из валют имеет отрицательный или нулевой курс"
        super().__init__(message)

class CurrencyNotFoundError(ExchangeError):
    def __init__(self, base: str):
        self.status_code = 404
        message = f"Не удалось найти валюту: '{base}'"
        super().__init__(message)

class NotFoundError(ExchangeError):
    def __init__(self):
        self.status_code = 404
        message = "Нет данных"
        super().__init__(message)

class CurrencyNotFoundIdError(ExchangeError):
    def __init__(self):
        self.status_code = 404
        message = f"Не удается найти идентификатор валюты"
        super().__init__(message)

class RateNotFoundError(ExchangeError):
    def __init__(self):
        self.status_code = 404
        message = ("База данных не содержит данных"
                    f" для конкретных валют")
        super().__init__(message)

class RatesNotFoundError(ExchangeError):
    def __init__(self):
        self.status_code = 404
        message = "База данных не содержит информации о курсах обмена валют"
        super().__init__(message) 

class AddCurrenciesError(ExchangeError):
    def __init__(self, base: str, target: str):
        self.status_code = 409
        message = f"Валютная пара с таким кодом ('{base}' -> '{target}') уже существует"
        super().__init__(message)

class AddCurrencyError(ExchangeError):
    def __init__(self, base: str):
        self.status_code = 409
        message = f"Валюта с кодом '{base}' уже существует"
        super().__init__(message)