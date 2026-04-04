from decimal import Decimal, getcontext, ROUND_DOWN
from exceptions import CurrencyNotFoundError
from utils import error_handler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dao import CurrencyDAO
    from services import ConvertRateService
    from dto import Currency

class ConvertService:
    def __init__(self, 
                 currency_dao: "CurrencyDAO", 
                 convert_rate_service: "ConvertRateService"):
        
        self._currency_dao = currency_dao
        self._convert_rate_service = convert_rate_service

    @error_handler
    def convert_currency(self, base_code: str, target_code: str, count_currency: str) -> dict[str, str | dict]:
        getcontext().rounding = ROUND_DOWN
        count_currency = abs(Decimal(str(count_currency)))    

        base_currency = self._currency_dao.get_currency(base_code)
        if base_currency is None:
            raise CurrencyNotFoundError(base_code)

        target_currency = self._currency_dao.get_currency(target_code)
        if target_currency is None:
            raise CurrencyNotFoundError(target_code)
        
        if base_code == target_code:
            return self._get_exchange_convert_amount(base_currency=base_currency, 
                                                     target_currency=target_currency, 
                                                     converted_amount=str(count_currency),
                                                     amount=str(count_currency))
        
        if count_currency == Decimal("0"):
            return self._get_exchange_convert_amount(base_currency=base_currency, 
                                                     target_currency=target_currency,
                                                     converted_amount="0",
                                                     amount=str(count_currency))
        
        rate_cross = self._convert_rate_service.get_conversion_rate(base_currency, target_currency)
        rate_cross_amount = str(round(rate_cross * count_currency, 6))
        
        return self._get_exchange_convert_amount(base_currency=base_currency, 
                                                 target_currency=target_currency,
                                                 converted_amount=rate_cross_amount, 
                                                 amount=str(count_currency))
    
    def _get_exchange_convert_amount(self, 
                                     base_currency: "Currency", 
                                     target_currency: "Currency", 
                                     converted_amount: str,
                                     amount: str) -> dict:
        rate_dict = {}
        rate_dict["baseCurrency"] = base_currency.to_dict()
        rate_dict["targetCurrency"] = target_currency.to_dict()
        rate_dict["amount"] = amount
        rate_dict["convertedAmount"] = converted_amount

        return rate_dict