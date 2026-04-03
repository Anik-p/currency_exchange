from http.server import BaseHTTPRequestHandler
from exceptions import ExchangeError
from handler.router import Router
from handler.front_mixin import FrontMixin
from exceptions import *
from urllib.parse import parse_qs, urlparse

class RequestHandler(BaseHTTPRequestHandler, FrontMixin):
    """
    HTTP обработчик для REST API обменника валют.
    
    Поддерживаемые методы:
    - GET: получение данных (списки, конкретные курсы, конвертация)
    - POST: создание новых валют и курсов
    - PATCH: обновление существующих курсов
    
    Формат ответов:
    {
        "code": 200,
        "body": {...} 
    }
    """
    def __init__(self, 
                 request, 
                 client_address, 
                 server,
                 router: Router):
        
        self.router = router
        super().__init__(request, client_address, server)

    def do_GET(self):
        """
        Обработчик GET запросов.
        
        Поддерживаемые endpoints:
        - GET /currencies - получить все валюты
        - GET /currency/USD - получить конкретную валюту
        - GET /exchangeRate/USDEUR - получить курс валютной пары
        - GET /convert?from=USD&to=EUR&amount=100 - конвертировать сумму

        Компоненты:
        -handler - экземпляр контроллера, полученный из router.resolve()
        -path_params - параметры запроса URL
        пример: /currency/USD -> {'code': 'USD'}
        - query_params: параметры из строки запроса после '?'
        пример: /convert?from=USD&to=EUR&amount=100 -> {'from': 'USD', 'to': 'EUR', 'amount': '100'}
        -params - объединенный словарь path_params + query_params
        -response - результат запроса handler(params)

        Обработка запросов:
        -Получение self.path от BaseHTTPRequestHandler
        -Разбиение self.path в self.router методом resolve, который возвращает (handler, path_params)
        -Инициализация params и добавление (если есть) в path_params
        -Получение query_params параметры запроса, если есть, добавляем в params
        -Вызываем handler(params) для получения response
        -Отправляем response в frontend через send_json()
        """
        try:
            handler, path_params = self.router.resolve(urlparse(self.path).path, method="GET")
            query_params = parse_qs(urlparse(self.path).query)
            params = {}
            if path_params:
                params.update(path_params)
            
            if query_params:
                query_params = {key: value[0] for key, value in query_params.items()}
                params.update(query_params)
            
            response = handler(params)
            self.send_json(response)
        except ExchangeError as err:
            response = {"code": err.status_code, "body": {"message": str(err)}}
            self.send_json(response)
        
    def do_POST(self):
        """
        POST запросы для создания ресурсов.
        Формат данных: application/x-www-form-urlencoded
        Для /currencies:
            name=US Dollar&code=USD&sign=$
        Для /exchangeRates:
            baseCurrencyCode=USD&targetCurrencyCode=EUR&rate=0.92
        """
        params = self.get_params()
        try:
            handler = self.router.resolve(self.path, method="POST")[0]
            response = handler(params)
            self.send_json(response)
        except ExchangeError as err:
            response = {"code": err.status_code, "body": {"message": str(err)}}
            self.send_json(response)

    def do_PATCH(self):
        """
        PATCH запрос для обновления курса.
        Пример: PATCH /exchangeRate/USDEUR
        body: rate=0.95
        Обновляет курс для валютной пары USDEUR
        """
        params = self.get_params()
        params['path'] = self.path
        try:
            handler = self.router.resolve(self.path, method='PATCH')[0]
            response = handler(params)
            self.send_json(response)
        except ExchangeError as err:
            response = {"code": err.status_code , "body": {"message": str(err)}}
            self.send_json(response)
        
    def get_params(self):
        """
        Извлекает параметры из тела POST/PATCH запроса.
        Поддерживаемый формат: application/x-www-form-urlencoded
        
        Обработка запросов:
        -Читает заголовок Content-Length для определения размера данных
        -Читает тело запроса через self.rfile.read()
        -Декодирует байты в строку UTF-8
        -Парсит строку в словарь через parse_qs()
        -Преобразует значения из списков в строки (берет первый элемент)

        Тело запроса: b'name=US Dollar&code=USD&sign=$' ->
    
        {'name': ['US Dollar'], 'code': ['USD'], 'sign': ['$']} ->
    
        Результат:
        {'name': 'US Dollar', 'code': 'USD', 'sign': '$'}
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        params = {key: value[0] for key, value in params.items()}
        return params