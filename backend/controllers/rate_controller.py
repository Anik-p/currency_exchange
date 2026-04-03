from exceptions import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import RateService, CurrencyService

class RateController:
    """
    Контроллер, отвечающий за вывод курса

    Получаемые данные:
        params:
            для get_rate
            Словарь с ключами:
                - 'pair' (str): коды валют (USDUSD)
            для register_exchange_rate_post
                - 'baseCurrencyCode' (str): код базовай валюты (USD)
                - 'targetCurrencyCode' (str): код рассчитываемой валюты (USD)
                - 'rate' (str): курс валют ('12.5')
            для register_exchange_rate_patch
                - path (str): коды валют (USD/USD)
                - rate (str): курс валют ('12.5')
            для get_all_rates нет поступаемых данных
    """
    def __init__(self, 
                 rate_service: "RateService", 
                 currency_service: "CurrencyService"):
         self._rate_service = rate_service
         self._currency_service = currency_service

    def get_rate(self, params: dict) -> dict:
        """
        GET /exchangeRate/{pair}
        Возвращает курс для валютной пары.
        return: {"code": 200, "body": {"id": 1, "baseCurrency": {...}, "targetCurrency": {...}, "rate": "0.92"}}
        """
        pair = params.get("pair")
        if not pair:
            raise NotFoundError
        if len(pair) != 6:
            raise NotFoundError
        base_code : str = pair[:3]
        target_code : str = pair[3:]
        if not (base_code and target_code):
            raise NotFoundError
             
        base_id = self._currency_service.get_currency(base_code).id
        target_id = self._currency_service.get_currency(target_code).id
        rate = self._rate_service.get_rate(base_id, target_id) 
        return {"code": 200, "body": rate.to_dict()}

    def get_all_rates(self, params: dict=None) -> dict:
        """
        GET /exchangeRates
        Возвращает список всех курсов обмена.
        """
        rates = self._rate_service.get_all_rate()
        return {"code": 200, "body": [rate.to_dict() for rate in rates if rate is not None]}

    def register_exchange_rate_post(self, params: dict) -> dict:
            """
            POST /exchangeRates
            Создает новый курс обмена.
            return {"code": 200, "body": {"id": 1, "baseCurrency": {...}, "targetCurrency": {...}, "rate": "0.92"}}
            """
            base_code: str = params.get("baseCurrencyCode")
            target_code: str = params.get("targetCurrencyCode")
            rate: str = params.get("rate")
            if not (base_code and target_code and rate):
                raise IncorrectCurrencyData
            
            if not (base_code.isalpha() and target_code.isalpha() and rate.replace('.', '').isdigit()):
                raise IncorrectInputCodeCurrency

            rate_post = self._rate_service.register_exchange_rate_post(base_code, target_code, rate) 
            return {"code": 200, "body": rate_post.to_dict()}
        
    def register_exchange_rate_patch(self, params: dict[str, str]) -> dict:
            """
            PATCH /exchangeRates
            Создает новый курс обмена.
            return {"code": 200, "body": {"id": 1, "baseCurrency": {...}, "targetCurrency": {...}, "rate": "0.92"}}
            """
            path = params.get("path")
            rate = params.get("rate")
            code = path.split("/")[-1]
            if len(code) != 6:
                 raise IncorrectInputCodeCurrency
            base_code = code[:3]
            target_code = code[3:]

            if not (base_code.isalpha() and target_code.isalpha() and rate.replace('.', '').isdigit()):
                 raise IncorrectInputCodeCurrency

            rate_patch = self._rate_service.register_exchange_rate_patch(base_code, target_code, rate) 
            return {"code": 200, "body": rate_patch.to_dict()}