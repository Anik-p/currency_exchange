from handler import RequestHandler, Router
from core import AppInitializer
from http.server import HTTPServer
from config import HOST, PORT

class Application:
    def __init__(self, initializer: AppInitializer):
        self.initializer = initializer
        self.router = Router()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.register("/currencies", "GET", self.initializer.currency_controller.get_all_currencies)
        self.router.register("/currency/(?P<code>[A-Z]{3})", "GET", self.initializer.currency_controller.get_currency)
        self.router.register("/exchangeRates", "GET", self.initializer.rate_controller.get_all_rates)
        self.router.register("/exchangeRate/(?P<pair>[A-Z]{6})", "GET", self.initializer.rate_controller.get_rate)
        self.router.register("/convert", "GET", self.initializer.convert_controller.convert)

        self.router.register("/currencies", "POST", self.initializer.currency_controller.register_currency)
        self.router.register("/exchangeRates", "POST", self.initializer.rate_controller.create_exchange_rate)

        self.router.register("/exchangeRate/(?P<pair>[A-Z]{6})", "PATCH", self.initializer.rate_controller.update_exchange_rate)    

    def create_request_handler(self, request, client_address, server):
        return RequestHandler(
            request=request,
            client_address=client_address,
            server=server,
            router=self.router)
    
    def run(self, host=HOST, port=PORT):
        server = HTTPServer((host, port), self.create_request_handler)
        print(f"Сервер запущен на {host}:{port}")
        server.serve_forever()