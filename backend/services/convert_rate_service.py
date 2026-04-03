from exceptions import RateNotFoundError, InvalidCrossRateError
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dto import ExchangeRate
    from dao import RateDAO
    from dto import Currency

class ConvertRateService:
    def __init__(self, rate_dao: RateDAO, usd_id: int):
        self._rate_dao = rate_dao
        self._usd_id = usd_id

    def get_conversion_rate(self, base_currency: Currency, target_currency: Currency) -> Decimal | None:

        rate = self._get_valid_rate(base_currency.id, target_currency.id)
   
        if rate is not None:
            return Decimal(rate.rate)
        
        reverse_rate = self._get_valid_rate(target_currency.id, base_currency.id)
        if reverse_rate is not None:
            return Decimal("1") / Decimal(reverse_rate.rate)

        cross_rate_base = self._find_direct_or_reverse(base_currency.id, self._usd_id)
        cross_rate_target = self._find_direct_or_reverse(self._usd_id, target_currency.id)

        if cross_rate_base is None or cross_rate_target is None:
            raise RateNotFoundError()
        
        return cross_rate_base * cross_rate_target
        
    def _get_valid_rate(self, base_id: int, target_id: int) -> ExchangeRate | None:
        rate = self._rate_dao.get_rate(base_id, target_id)

        if rate is None:
            return None
        
        if Decimal(rate.rate) <= Decimal("0"):
            raise InvalidCrossRateError
        
        return rate
        
    def _find_direct_or_reverse(self, base_id: int, target_id: int) -> Decimal | None:
        rate = self._get_valid_rate(base_id, target_id)
        if rate is not None:
            return Decimal(rate.rate)
         
        rate_reverse = self._rate_dao.get_rate(target_id, base_id)

        if rate_reverse is None:
            return None
         
        return Decimal("1") / Decimal(rate_reverse.rate)