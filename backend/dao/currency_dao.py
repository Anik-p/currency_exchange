from exceptions import DatabaseOperationError, CurrencyNotFoundError, NotFoundError, CurrencyNotFoundIdError, AddCurrencyError
from utils.error_handler_dao import error_handler_dao
from dto import Currency
import sqlite3

class CurrencyDAO:
    def __init__(self, path_db: str):
        self._path_db = path_db

    @error_handler_dao
    def get_currency(self, code: str) -> Currency:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
            row = cursor.fetchone()
            if row is None:
                raise CurrencyNotFoundError(code)
            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])

    @error_handler_dao    
    def get_currency_by_id(self, base_id: int) -> Currency:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies WHERE ID = ?", (base_id,))
            row = cursor.fetchone()
            if row is None:
                raise CurrencyNotFoundIdError
            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])

    @error_handler_dao    
    def get_all_currencies(self) -> list[Currency]:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies")
            all_row = cursor.fetchall()
            if not all_row:
                raise NotFoundError
            return [Currency(id=row["ID"],
                                code=row["Code"],
                                name=row["FullName"],
                                sign=row["Sign"])
                        for row in all_row]

    @error_handler_dao
    def create_currency(self, name: str, code: str, sign: str) -> Currency:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)", (code, name, sign))
                conn.commit()
                cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
                row = cursor.fetchone()
            except sqlite3.IntegrityError:
                raise AddCurrencyError(code)

            if row is None:
                raise DatabaseOperationError

            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])    