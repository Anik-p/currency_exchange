from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dto import Currency
    from dao import CurrencyDAO

class CurrencyService:
    def __init__(self, currency_dao: CurrencyDAO):
        self._currency_dao = currency_dao

    def get_currency_via_id(self, base_id: int):
        return self._currency_dao.get_currency_by_id(base_id)

    def get_currency(self, code: str):
        return self._currency_dao.get_currency(code)
    
    def get_all_currencies(self):
        return self._currency_dao.get_all_currencies()
    
    def register_currency(self, name: str, code: str, sign: str) -> Currency:
        return self._currency_dao.create_currency(name, code, sign)