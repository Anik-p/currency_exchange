import sqlite3
from pathlib import Path
from config import DB_PATH

def delete_table():
    DB = Path(DB_PATH).resolve()
    if not DB.exists():
        return ("Таблицы в базе данных уже удалены")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    current_dir = Path(__file__).parent.resolve()
    file = current_dir / "delete.sql"

    with open(file, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    return ("Таблицы в базе данных удалены")