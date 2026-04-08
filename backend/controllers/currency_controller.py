from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import CurrencyService
    from utils import InputValidator

class CurrencyController:
    """
     Контроллер для работы с валютами.
    
    Эндпоинты:
    - GET /curules/{code} - получение валюты по коду
    - GET /currencies - получение всех валют
    - POST /currencies - создание новой валюты
    """
    def __init__(self, 
                 currency_service: CurrencyService, 
                 validator: InputValidator):
        
        self._currency_service = currency_service
        self._validator = validator

    def get_currency(self, params: dict) -> dict:
        """
        GET /currency/{code}
        Возвращает информацию о валюте по её коду.
        Returns:
            dict: {"code": 200, "body": {...}}
            
        Example response:
            {
                "id": 1,
                "name": "United States dollar",
                "code": "USD",
                "sign": "$"
            }
        """
        code = params.get("code")
        currency = self._currency_service.get_currency(code)
        return {"code": 200, "body": currency.to_dict()}
    
    def get_all_currencies(self, params: dict=None) -> dict:
        """
        GET /currencies
        Возвращает список всех валют.
        Return: {"code": 200, "body": [{"id": 1, ...}, ...]}
        """
        currencies = self._currency_service.get_all_currencies()
        return {"code": 200, "body": [curr.to_dict() for curr in currencies]}

    def register_currency(self, params: dict) -> dict:
        """
        POST /currencies
        Создает новую валюту.
        params: Данные формы с ключами:
                - 'code' (str): Код валюты (3 буквы)
                - 'name' (str): Полное название валюты
                - 'sign' (str): Символ валюты ($, €, ₽)
                
        Returns:
            dict: {"code": 201, "body": {...}}
        """

        code: str = params.get("code")
        name: str = params.get("name")
        sign: str = params.get("sign")
        
        self._validator.validate_currency(code, name, sign)
        correct_name = name.lower().title()
        correct_code = code.upper()

        currency = self._currency_service.register_currency(correct_name, correct_code, sign)
        return {"code": 201, "body": currency.to_dict()}