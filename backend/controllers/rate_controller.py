from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import RateService, CurrencyService
    from utils import InputValidator

class RateController:
    """
    Контроллер, отвечающий за вывод курса

    Контроллер для работы с курсами обмена.
    
    Эндпоинты:
    - GET /exchangeRate/{pair} - получение курса по паре валют
    - GET /exchangeRates - получение всех курсов
    - POST /exchangeRates - создание нового курса
    - PATCH /exchangeRate/{pair} - обновление курса
    """
    def __init__(self, 
                 rate_service: RateService, 
                 currency_service: CurrencyService,
                 validator: InputValidator):
         
         self._rate_service = rate_service
         self._currency_service = currency_service
         self._validator = validator


    def get_rate(self, params: dict) -> dict:
        """
        GET /exchangeRate/{pair}
        Получение курса для валютной пары.
        
        Args:
            path_params: Параметры пути {'pair': 'USDEUR'}
            
        Returns:
            dict: {"code": 200, "body": {...}}
        """
        pair = self._validator.extract_currency_pair(params.get("pair"))
        base_code, target_code = pair
             
        base_id = self._currency_service.get_currency(base_code).id
        target_id = self._currency_service.get_currency(target_code).id
        rate = self._rate_service.get_rate(base_id, target_id) 
        return {"code": 200, "body": rate.to_dict()}

    def get_all_rates(self, params: dict=None) -> dict:
        """
        GET /exchangeRates
        Получение списка всех курсов обмена.
        
        Returns:
            dict: {"code": 200, "body": [...]}
        """
        rates = self._rate_service.get_all_rates()
        return {"code": 200, "body": [rate.to_dict() for rate in rates]}

    def create_exchange_rate(self, params: dict) -> dict:
        """
        POST /exchangeRates
        Создает новый курс обмена.
        params: Данные формы с ключами:
            - 'baseCurrencyCode' (str): Код базовой валюты
            - 'targetCurrencyCode' (str): Код целевой валюты
            - 'rate' (str): Курс обмена
                
        Returns:
            dict: {"code": 201, "body": {...}}
        """
        base_code: str = params.get("baseCurrencyCode")
        target_code: str = params.get("targetCurrencyCode")
        rate: str = params.get("rate")
        self._validator.validate_rate(base_code, target_code, rate)

        rate_post = self._rate_service.create_exchange_rate(base_code, target_code, rate) 
        return {"code": 201, "body": rate_post.to_dict()}
        
    def update_exchange_rate(self, params: dict[str, str]) -> dict:
        """
        PATCH /exchangeRate/{pair}
        
        Обновление существующего курса обмена.

        path_params: Параметры пути {'pair': 'USDEUR'}
        form_data: Данные формы с ключом 'rate'
            
        Returns:
            dict: {"code": 200, "body": {...}}
        """
        path = params.get("path")
        rate = params.get("rate")
        code = self._validator.extract_currency_pair(path.split("/")[-1])
        base_code, target_code = code
        self._validator.validate_rate(base_code, target_code, rate)

        rate_patch = self._rate_service.update_exchange_rate(base_code, target_code, rate) 
        return {"code": 200, "body": rate_patch.to_dict()}