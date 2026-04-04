from __future__ import annotations
from exceptions import IncorrectCurrencyData, IncorrectInputCodeCurrency
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import CurrencyService

class CurrencyController:
    """
    Контроллер, отвечающий за вывод списка или конкретной валюты и ее регистрации
    Получаемые данные:
        params: 
            для register_currency:
                Словарь с ключами:
                - 'name' (str): Название исходной валюты (например, 'USD')
                - 'code' (str): Код исходной валюты (например, 'EUR')
                - 'sing' (str): Знак исходной валюты  
            для get_currency:
                - 'code' (str): Код исходной валюты (например, 'EUR')
            для get_all_currency нет поступаемых данных
    """
    def __init__(self, currency_service: CurrencyService):
        self._currency_service = currency_service

    def get_currency(self, params: dict) -> dict:
        """
        GET /currency/{code}
        Возвращает информацию о валюте по её коду.
        params: {'code': 'USD'}
        Return: {"code": 200, "body": {"id": 1, "code": "USD", ...}}
        """
        code = params.get("code")
        currency = self._currency_service.get_currency(code)
        return {"code": 200, "body": currency.to_dict()}
    
    def get_all_currency(self, params: dict=None) -> dict:
        """
        GET /currencies
        Возвращает список всех валют.
        Return: {"code": 200, "body": [{"id": 1, ...}, ...]}
        """
        currencies = self._currency_service.all_get_currency()
        return {"code": 200, "body": [curr.to_dict() for curr in currencies if curr is not None]}

    def register_currency(self, params: dict) -> dict:
        """
        POST /currencies
        Создает новую валюту.
        Return: {"code": 200, "body": {"id": 123, ...}}
        """
        name: str = params.get("name") 
        code: str = params.get("code")
        sign: str = params.get("sign")
        if not (name and code and sign): 
            raise IncorrectCurrencyData
        
        if not (name.isalpha() and code.isalpha() and len(code)== 3):
                raise IncorrectInputCodeCurrency

        currency = self._currency_service.register_currency(name, code, sign)
        return {"code": 200, "body": currency.to_dict()}