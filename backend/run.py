from controllers import ServerApp
from config.base_config import DB_PATH
from db import *
from core import AppInitializer
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def setup_db():
    if Path(DB_PATH).exists():
        while True:
            print("База данных уже существует. Перезаписать БД? (y/n)")
            value = input()
            if value == "y":
                print(delete_table())
                print(create_table())
                break
            if value == "n":
                break
            print("Введите 'y' или 'n'")
    else:
        print("Инициализация БД...")
        print(init_db())
        
if __name__ == "__main__":
    setup_db()
    initializer = AppInitializer()
    app = ServerApp(initializer)
    try:
        logging.info("Запуск сервера...")
        app.run()
    except KeyboardInterrupt:
        logging.info("Сервер остановлен пользователем...")
    except SystemExit:
        logging.info("Программа завершает свою работу...")
    except Exception as err:
        logging.exception("Произошла непредвиденная ошибка: %s", err)
    finally:
        logging.info("Завершение соединения")