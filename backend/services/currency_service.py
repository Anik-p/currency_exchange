from __future__ import annotations
from exceptions import CurrencyNotFoundError, CurrenciesNotFoundError, CurrencyPairInputError
from utils import error_handler

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dto import Currency
    from dao import CurrencyDAO

class CurrencyService:
    def __init__(self, currency_dao: CurrencyDAO):
        self._currency_dao = currency_dao

    @error_handler
    def get_currency_via_id(self, base_id: int):
        currency = self._currency_dao.get_currency_via_id(base_id)
        if currency is None:
            return None
        return currency

    @error_handler
    def get_currency(self, code: str):
        currency = self._currency_dao.get_currency(code)
        if currency is None:
            raise CurrencyNotFoundError(code)
        return currency
    
    @error_handler
    def all_get_currency(self):
        all_currency = self._currency_dao.all_get_currency()
        if all_currency is None:
            raise CurrenciesNotFoundError()
        return all_currency
    
    @error_handler
    def register_currency(self, name: str, code: str, sign: str) -> Currency:
        currency = self._currency_dao.register_currency_post(name, code, sign)
        if currency is None:
            raise CurrencyPairInputError()
        return currency