from pathlib import Path

HOST = "0.0.0.0"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "exchange.db"