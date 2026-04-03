import sqlite3
from pathlib import Path
from config import DB_PATH

def create_table():

    DB = Path(DB_PATH).resolve()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    current_dir = Path(__file__).parent.resolve()
    
    file_seed = current_dir / "seed.sql"
    file_rate = current_dir / "rate.sql"

    with open(file_seed, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    with open(file_rate, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()

    return ("Таблицы созданы")