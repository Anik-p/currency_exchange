from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import ConvertService
    from utils import InputValidator
    from decimal import Decimal

class ConvertController:
    """Класс, отвечающий за конвертацию валюты.
        Получаемые данные:
            request: Словарь с ключами:
                - 'from' (str): Код исходной валюты (например, 'USD')
                - 'to' (str): Код целевой валюты (например, 'EUR')
                - 'amount' (str): Сумма для конвертации
    """
    def __init__(self, 
                 convert_service: ConvertService, 
                 validator: InputValidator):
        
        self._convert_service = convert_service
        self._validator = validator

    def convert(self, params: dict) -> dict[str, dict]:
        """
        GET /convert?from={from}&to={to}&amount={amount}
        Конвертирует сумму из одной валюты в другую.
        Return:
            {
                "code": 200,
                "body": {
                    "baseCurrency": {...},
                    "targetCurrency": {...},
                    "amount": "100",
                    "convertedAmount": "92.00"
                }
            }
        """
        from_code: str = params.get("from")
        to_code: str = params.get("to")
        amount: Decimal = self._validator.validate_convert(params.get("amount")) 
        
        result = self._convert_service.convert_currency(from_code, to_code, amount)
        return {"code": 200, "body": result}