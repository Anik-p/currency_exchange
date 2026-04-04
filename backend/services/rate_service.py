from __future__ import annotations
from exceptions import *
from dto import ExchangeRateCurrencies, ExchangeRate
from utils import error_handler
from typing import TYPE_CHECKING
from services import CurrencyService

if TYPE_CHECKING:
    from dao import RateDAO

class RateService:
    def __init__(self, 
                 currency_service: CurrencyService, 
                 rate_dao: RateDAO
                 ):
        
        self._currency_service = currency_service
        self._rate_dao = rate_dao
        
    @error_handler
    def register_exchange_rate_post(self, base_code: str, target_code: str, rate: str) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.create_exchange_rate(base_code, target_code, rate)
        if exchange_rate is None:
            raise AddCurrenciesError(base_code, target_code)
        return self._get_exchange_rate_currency(exchange_rate)

    @error_handler
    def register_exchange_rate_patch(self, base_code: str, target_code: str, rate: str) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.update_exchange_rate(base_code, target_code, rate)
        if exchange_rate is None:
            raise InvalidRateError(base_code, target_code)
        return self._get_exchange_rate_currency(exchange_rate)

    @error_handler
    def get_rate(self, base_id: int, target_id: int) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.get_rate(base_id, target_id)
        if exchange_rate is None:
            raise RateNotFoundError()
        return self._get_exchange_rate_currency(exchange_rate)
    
    @error_handler
    def get_all_rate(self) -> list[ExchangeRateCurrencies]:
        all_rate = self._rate_dao.get_all_rate()
        return [self._get_exchange_rate_currency(rate) for rate in all_rate if rate is not None]
    
    def _get_exchange_rate_currency(self, exchange_rate: ExchangeRate) -> ExchangeRateCurrencies:
        base_currency = self._currency_service.get_currency_via_id(exchange_rate.base_id)
        target_currency = self._currency_service.get_currency_via_id(exchange_rate.target_id)
        if base_currency is None or target_currency is None:
            raise CurrencyPairInputError
        return ExchangeRateCurrencies(id=exchange_rate.id,
                                    base_currency=base_currency,
                                    target_currency=target_currency,
                                    rate=exchange_rate.rate)