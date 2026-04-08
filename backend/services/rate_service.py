from __future__ import annotations
from dto import ExchangeRateCurrencies, ExchangeRate
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
        
    def create_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.create_exchange_rate(base_code, target_code, rate)
        return self._get_exchange_rate_currency(exchange_rate)

    def update_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.update_exchange_rate(base_code, target_code, rate)
        return self._get_exchange_rate_currency(exchange_rate)

    def get_rate(self, base_id: int, target_id: int) -> ExchangeRateCurrencies:
        exchange_rate = self._rate_dao.get_rate(base_id, target_id)
        return self._get_exchange_rate_currency(exchange_rate)
    
    def get_all_rates(self) -> list[ExchangeRateCurrencies]:
        all_rate = self._rate_dao.get_all_rates()
        return [self._get_exchange_rate_currency(rate) for rate in all_rate]
    
    def _get_exchange_rate_currency(self, exchange_rate: ExchangeRate) -> ExchangeRateCurrencies:
        base_currency = self._currency_service.get_currency_via_id(exchange_rate.base_id)
        target_currency = self._currency_service.get_currency_via_id(exchange_rate.target_id)
        return ExchangeRateCurrencies(id=exchange_rate.id,
                                    base_currency=base_currency,
                                    target_currency=target_currency,
                                    rate=exchange_rate.rate)