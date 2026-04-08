from exceptions import NotFoundError
from typing import Callable
import re

class Router:
    """
    Машрутизатор HTTP запросов
    """
    def __init__(self):
        self.__endpoints = {"GET": {}, "POST": {}, "PATCH": {}}

    def register(self, path: str, method: str, handler: Callable) -> Callable:
        """Регистратор новых маршрутов
        path (str): URL паттерн с поддержкой regex
        method (str): HTTP метод ("GET", "POST", "PATCH")
        handler (Callable): Функция-обработчик (метод контроллера)
        """
        self.__endpoints[method][re.compile(path)] = handler
        return handler

    def resolve(self, path: str, method: str) -> tuple[Callable]:
        """
        Обработчик пути и HTTP метода
        path (str): URL паттерн с поддержкой regex групп
        method (str): HTTP метод ("GET", "POST", "PATCH")
        handler (Callable): Функция-обработчик (метод контроллера)
        """
        
        for url, handler in self.__endpoints[method].items():
            match = url.match(path)
            if match:
                return handler, match.groupdict()
        
        raise NotFoundError()