from dto import ExchangeRate
import sqlite3

class RateDAO:
    def __init__(self, path_db: str):
        self._path_db = path_db

    def get_rate(self, base_id: int, target_id: int) -> ExchangeRate | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ExchangeRates "
                            "WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (base_id, target_id))
            row = cursor.fetchone()
            if row is None:
                return None
            
            return ExchangeRate(id=row["ID"],
                                base_id=row["BaseCurrencyId"],
                                target_id=row["TargetCurrencyId"],
                                rate=str(row["Rate"]))
        
    def get_all_rate(self) -> list[ExchangeRate] | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ExchangeRates")
            all_row = cursor.fetchall()
                
            return [ExchangeRate(id=row["ID"],
                                     base_id=row["BaseCurrencyId"],
                                     target_id=row["TargetCurrencyId"],
                                     rate=str(row["Rate"])) for row in all_row]
            
    def create_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRate | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM Currencies WHERE Code = ?", (base_code,))
            row_base = cursor.fetchone()
            cursor.execute("SELECT ID FROM Currencies WHERE Code = ?", (target_code,))
            row_target = cursor.fetchone()
            if row_base is None or row_target is None:
                return None
            
            base_id = row_base["ID"]
            target_id = row_target["ID"]

            cursor.execute("SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (base_id, target_id))
            existing = cursor.fetchone()
            if existing is not None:
                return None
            
            cursor.execute("INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)", (base_id, target_id, rate))   
            conn.commit()
            cursor.execute("SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? and TargetCurrencyId = ?", (base_id, target_id))
            row = cursor.fetchone()

            if row is None:
                return None

            return ExchangeRate(id=row["ID"],
                                base_id=row["BaseCurrencyId"],
                                target_id=row["TargetCurrencyId"],
                                rate=row["Rate"])
        
    def update_exchange_rate(self, base_code: str, target_code: str, rate: str) -> ExchangeRate:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM Currencies WHERE Code = ?", (base_code,))
            row_base = cursor.fetchone()
            cursor.execute("SELECT ID FROM Currencies WHERE Code = ?", (target_code,))
            row_target = cursor.fetchone()
            if row_base is None or row_target is None:
                return None

            base_id = row_base["ID"]
            target_id = row_target["ID"]

            cursor.execute("SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (base_id, target_id))
            
            existing = cursor.fetchone()
            if existing is None:
                return None
            
            cursor.execute("UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (rate, base_id, target_id))
            conn.commit()
            cursor.execute("SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? and TargetCurrencyId = ?", (base_id, target_id))
            row = cursor.fetchone()

            if row is None:
                return None   

            return ExchangeRate(id=row["ID"],
                                base_id=row["BaseCurrencyId"],
                                target_id=row["TargetCurrencyId"],
                                rate=row["Rate"])