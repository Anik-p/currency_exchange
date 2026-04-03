from controllers import ServerApp
from config.base_config import DB_PATH
from db import *
from core import AppInitializer
from pathlib import Path

if __name__ == "__main__":
    if Path(DB_PATH).exists():
        while True:
            print("Перезаписать БД? (y/n)")
            value = input()
            if value == "y":
                print(delete_table())
                print(create_table())
                break
            if value == "n":
                break
            print("Введите y/n")
    else:
        print("Инициализация БД...")
        print(init_db())

    initializer = AppInitializer()
    app = ServerApp(initializer)
    app.run()