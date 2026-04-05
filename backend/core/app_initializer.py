from controllers import ConvertController, CurrencyController, RateController
from services import ConvertService, CurrencyService, ConvertRateService, RateService
from dao import CurrencyDAO, RateDAO
from config.base_config import DB_PATH
from exceptions import *
from pathlib import Path

class AppInitializer:
    def __init__(self):
        self._app_init()

    def _app_init(self):
        self._init_dao()
        self._init_service()
        self._init_controller()

    def _path_db(self):
        relative_path = DB_PATH
        try:
            return Path(relative_path).resolve()
        except FileNotFoundError:
            raise DatabaseUnavailableError()

    def _init_dao(self):
        path_db = self._path_db()
        self.currency_dao = CurrencyDAO(path_db)
        self.rate_dao = RateDAO(path_db)

    def _init_service(self):
        self.currency_service = CurrencyService(self.currency_dao)
        usd_id = self._get_value_id_usd()
        self.convert_rate_service = ConvertRateService(self.rate_dao, usd_id)
        self.convert_service = ConvertService(self.currency_dao, self.convert_rate_service)
        self.rate_service = RateService(self.currency_service, self.rate_dao)

    def _get_value_id_usd(self):
        usd_currency = self.currency_dao.get_currency("USD")
        if usd_currency is None:
            raise CurrencyNotFoundError("USD")
        return usd_currency.id
        
    def _init_controller(self):
        self.convert_controller = ConvertController(self.convert_service)
        self.currency_controller = CurrencyController(self.currency_service)
        self.rate_controller = RateController(self.rate_service, self.currency_service)