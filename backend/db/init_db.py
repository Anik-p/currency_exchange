import sqlite3
from pathlib import Path
from config import DB_PATH

def init_db():
    DB = Path(DB_PATH).resolve()
    if DB.exists():
        return("База данных уже инициализирована")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    current_dir = Path(__file__).parent.resolve()
    
    file_schema = current_dir / "schema.sql"
    file_seed = current_dir / "seed.sql"
    file_rate = current_dir / "rate.sql"

    with open(file_schema, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    with open(file_seed, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    with open(file_rate, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    return ("База данных создана и инициализирована")