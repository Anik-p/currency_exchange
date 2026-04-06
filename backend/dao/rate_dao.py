from __future__ import annotations
from exceptions import DatabaseOperationError, RateNotFoundError, AddCurrenciesError, NotFoundError
from dto import ExchangeRate
from utils.dao_guard import error_handler_dao
import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dao import CurrencyDAO

class RateDAO:
    def __init__(self, 
                 currency_dao: CurrencyDAO, 
                 path_db: str):
        
        self._currency_dao = currency_dao
        self._path_db = path_db

    @error_handler_dao
    def get_rate(self, base_id: int, target_id: int) -> ExchangeRate:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ExchangeRates "
                            "WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (base_id, target_id))
            row = cursor.fetchone()
            if row is None:
                raise RateNotFoundError
            return ExchangeRate(id=row["ID"],
                                base_id=row["BaseCurrencyId"],
                                target_id=row["TargetCurrencyId"],
                                rate=str(row["Rate"]))

    @error_handler_dao    
    def get_all_rate(self) -> list[ExchangeRate]:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ExchangeRates")
            all_row = cursor.fetchall()
            if all_row is None:
                raise NotFoundError
            return [ExchangeRate(id=row["ID"],
                                     base_id=row["BaseCurrencyId"],
                                     target_id=row["TargetCurrencyId"],
                                     rate=str(row["Rate"])) for row in all_row]

    @error_handler_dao        
    def create_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRate:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            base_id = self._currency_dao.get_currency(base_code).id
            target_id = self._currency_dao.get_currency(target_code).id
            try:
                cursor.execute("INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)", (base_id, target_id, rate))   
                conn.commit()
            except sqlite3.IntegrityError:
                raise AddCurrenciesError(base_code, target_code)
            if cursor.lastrowid == 0:
                raise DatabaseOperationError
            return self.get_rate(base_id, target_id)

    @error_handler_dao    
    def update_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRate:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            base_id = self._currency_dao.get_currency(base_code).id
            target_id = self._currency_dao.get_currency(target_code).id

            cursor.execute("SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (base_id, target_id))
            existing = cursor.fetchone()
            if existing is None:
                raise RateNotFoundError
            cursor.execute("UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (rate, base_id, target_id))
            conn.commit()

            return self.get_rate(base_id, target_id)