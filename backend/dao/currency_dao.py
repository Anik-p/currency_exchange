from dto import Currency
import sqlite3

class CurrencyDAO:
    def __init__(self, path_db: str):
        self._path_db = path_db

    def get_currency(self, code: str) -> Currency | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])
        
    def get_currency_via_id(self, base_id: int) -> Currency | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies WHERE ID = ?", (base_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])
        
    def all_get_currency(self) -> list[Currency] | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies")
            all_row = cursor.fetchall()
            if not all_row:
                return None
            return [Currency(id=row["ID"],
                                code=row["Code"],
                                name=row["FullName"],
                                sign=row["Sign"])
                        for row in all_row]

    def register_currency_post(self, name: str, code: str, sign: str) -> Currency | None:
        with sqlite3.connect(self._path_db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
            control_row = cursor.fetchone()
            if control_row is not None:
                return None
            
            cursor.execute("INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)", (code, name, sign))
            conn.commit()
            cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Currency(id=row["ID"],
                            code=row["Code"],
                            name=row["FullName"],
                            sign=row["Sign"])    