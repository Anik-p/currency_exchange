from __future__ import annotations
from utils import error_handler_dao

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dto import Currency
    from dao import CurrencyDAO

class CurrencyService:
    def __init__(self, currency_dao: CurrencyDAO):
        self._currency_dao = currency_dao

    def get_currency_via_id(self, base_id: int):
        currency = self._currency_dao.get_currency_via_id(base_id)
        return currency

    def get_currency(self, code: str):
        currency = self._currency_dao.get_currency(code)
        return currency
    
    def all_get_currency(self):
        all_currency = self._currency_dao.all_get_currency()
        return all_currency
    
    def register_currency(self, name: str, code: str, sign: str) -> Currency:
        currency = self._currency_dao.register_currency_post(name, code, sign)
        return currency