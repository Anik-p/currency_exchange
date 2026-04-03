from exceptions import ExchangeError

class IncorrectCurrencyData(ExchangeError):
    status_code = 400
    def __init__(self):
        message = "Обязательное поле формы отсутствует"
        super().__init__(message)

class IncorrectInputCodeCurrency(ExchangeError):
    status_code = 400
    def __init__(self):
        message = "Данный ввод валюты не корректен"
        super().__init__(message)

class CurrenciesNotFoundError(ExchangeError):
    status_code = 400
    def __init__(self):
        message = "Библиотечная база данных не содержит данных о валюте"
        super().__init__(message) 

class InvalidCurrencyError(ExchangeError):
    status_code = 400
    def __init__(self, base: str):
        message = f"Неизвестный код валюты'{base}'"
        super().__init__(message)

class InvalidAmountError(ExchangeError):
    status_code = 400
    def __init__(self):
        message = "Неправильный расчет обменного курса"
        super().__init__(message)   

class CurrencyPairInputError(ExchangeError):
    status_code = 400
    def __init__(self):
        message = (f"В адресе отсутствуют коды валют данной пары")
        super().__init__(message)

class InvalidRateError(ExchangeError):
    status_code = 400
    def __init__(self, base: str, target: str):
        message = f"Невозможно рассчитать обменный курс для '{base}' и '{target}'"
        super().__init__(message)

class InvalidCrossRateError(ExchangeError):
    status_code = 403
    def __init__(self):
        message = f"Невозможно рассчитать кросс курс, поскольку одна из валют имеет отрицательный или нулевой курс"
        super().__init__(message)

class CurrencyNotFoundError(ExchangeError):
    status_code = 404
    def __init__(self, base: str):
        message = f"Не удалось найти валюту: '{base}'"
        super().__init__(message)

class NotFoundError(ExchangeError):
    status_code = 404
    def __init__(self):
        message = "Нет данных"
        super().__init__(message)

class CurrencyNotFoundIdError(ExchangeError):
    status_code = 404
    def __init__(self, base: str):
        message = f"Не удается найти идентификатор валюты: {base}"
        super().__init__(message)

class RateNotFoundError(ExchangeError):
    status_code = 404
    def __init__(self):
        message = ("База данных не содержит данных"
                    f" для конкретных валют")
        super().__init__(message)

class RatesNotFoundError(ExchangeError):
    status_code = 404
    def __init__(self):
        message = "База данных не содержит информации о курсах обмена валют"
        super().__init__(message) 

class AddCurrenciesError(ExchangeError):
    status_code = 409
    def __init__(self, base: str, target: str):
        message = f"Валютная пара с таким кодом ('{base}' -> '{target}') уже существует"
        super().__init__(message)

class AddCurrencyError(ExchangeError):
    status_code = 409
    def __init__(self, base: str):
        message = f"Валюта, в которой указан этот код '{base}' уже существует"
        super().__init__(message)