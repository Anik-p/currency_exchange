from dto.currency import Currency 
from dataclasses import dataclass

@dataclass(frozen=True)
class ExchangeRateCurrencies:
    id: int
    base_currency: Currency
    target_currency: Currency
    rate: str

    def to_dict(self) -> dict:
        return {"id": self.id,
                "baseCurrency": self.base_currency.to_dict(),
                "targetCurrency": self.target_currency.to_dict(),
                "rate": self.rate}

@dataclass(frozen=True)
class ExchangeRate:
    id: int
    base_id: int
    target_id: int
    rate: str