from exceptions import *
import sqlite3
import functools

def error_handler(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as err:
                raise DatabaseUnavailableError(str(err))
            except sqlite3.DatabaseError as err:
                raise StorageError(str(err))
        return wrapper