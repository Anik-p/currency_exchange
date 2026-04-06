from __future__ import annotations
from typing import TYPE_CHECKING
from exceptions import IncorrectInputCodeCurrency

if TYPE_CHECKING:
    from services import ConvertService

class ConvertController:
    """Класс, отвечающий за конвертацию валюты.
        Получаемые данные:
            request: Словарь с ключами:
                - 'from' (str): Код исходной валюты (например, 'USD')
                - 'to' (str): Код целевой валюты (например, 'EUR')
                - 'amount' (str): Сумма для конвертации
    """
    def __init__(self, convert_service: ConvertService,):
        self._convert_service = convert_service

    def convert(self, request: dict) -> dict[str, dict]:
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
        code_base: str = request.get("from")
        code_target: str = request.get("to")
        amount: str = request.get("amount")
        if not (code_base.isalpha() and code_target.isalpha() and amount.replace('.', '').isdigit()):
            raise IncorrectInputCodeCurrency
        
        convert_rate = self._convert_service.convert_currency(code_base, code_target, amount)
        return {"code": 200, "body": convert_rate}