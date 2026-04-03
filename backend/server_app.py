from handler import RequestHandler, Router
from core import AppInitializer
from http.server import HTTPServer
from config import HOST, PORT

class ServerApp:
    def __init__(self, initializer: AppInitializer):
        self.initializer = initializer
        self.router = Router()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.dispatch("/currencies", "GET", self.initializer.currency_controller.get_all_currency)
        self.router.dispatch("/currency/(?P<code>[A-Z]{3})", "GET", self.initializer.currency_controller.get_currency)
        self.router.dispatch("/exchangeRates", "GET", self.initializer.rate_controller.get_all_rates)
        self.router.dispatch("/exchangeRate/(?P<pair>[A-Z]{6})", "GET", self.initializer.rate_controller.get_rate)
        self.router.dispatch("/convert", "GET", self.initializer.convert_controller.convert)

        self.router.dispatch("/currencies", "POST", self.initializer.currency_controller.register_currency)
        self.router.dispatch("/exchangeRates", "POST", self.initializer.rate_controller.register_exchange_rate_post)

        self.router.dispatch("/exchangeRate/(?P<pair>[A-Z]{6})", "PATCH", self.initializer.rate_controller.register_exchange_rate_patch)    

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