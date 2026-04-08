from exceptions import DatabaseUnavailableError, StorageError
import sqlite3
from functools import wraps


def error_handler_dao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.OperationalError as err:
            raise DatabaseUnavailableError(str(err))
        except sqlite3.DatabaseError as err:
            raise StorageError(str(err))
        
    return wrapper