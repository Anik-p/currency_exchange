from config.validation_constants import LEN_CODE, LEN_NAME, LEN_SIGN, MAX_RATE, MIN_RATE, MAX_AMOUNT
from decimal import Decimal, InvalidOperation
from pathlib import Path
from exceptions import IncorrectInputCodeCurrency, IncorrectCurrencyData, DataBaseValidatorError

class InputValidator:

    def __init__(self):
        self.word = self._profanity_words()

    def _profanity_words(self) -> list:
        dir_path = Path(__file__).parent.resolve()
        data_ru = dir_path / "data" / "ru.txt"
        data_en = dir_path / "data"  / "en.txt"

        if not data_ru.exists():
            raise DataBaseValidatorError("ru.txt")
        if not data_en.exists():
            raise DataBaseValidatorError("en.txt")
            
        set_words = set()        
        with open(data_ru, "r", encoding="utf-8") as f:
            set_words.update([row.strip().lower() for row in f.readlines()])
                
        with open(data_en, "r", encoding="utf-8") as f:
            set_words.update([row.strip().lower() for row in f.readlines()])
        
        return set_words
    
    def validate_currency(self, code: str, name: str, sign: str) -> None:
        if not (code and name and sign):
            raise IncorrectCurrencyData

        if not all([row.isalpha() for row in name.split()]):
            raise IncorrectInputCodeCurrency("Название валюты должно состоять из букв")

        if not code.isalpha():
            raise IncorrectInputCodeCurrency("Код валюты должен состоять из букв")
            
        if not len(code) == LEN_CODE:
            raise IncorrectInputCodeCurrency(f"Длина кода должна составлять '{LEN_CODE}' символа")
            
        if not len(name) <= LEN_NAME:
            raise IncorrectInputCodeCurrency(f"Название валюты слишком длинное, не более {LEN_NAME} символов")
            
        if not len(sign) <= LEN_SIGN:
            raise IncorrectInputCodeCurrency(f"Длина знака слишком большая, не более {LEN_SIGN} символов")
        
        if self._validate_profanity_words(code):
            raise IncorrectInputCodeCurrency(f"Введенное слово в 'code': ({code}) является нецензурным")
        
        if self._validate_profanity_words(name):
            raise IncorrectInputCodeCurrency(f"Введенное слово в 'name': ({name}) является нецензурным")
        
        if self._validate_profanity_words(sign):
            raise IncorrectInputCodeCurrency(f"Введенное слово в 'sign': ({sign}) является нецензурным")
        
    def validate_rate(self, base_code: str, target_code: str, rate: str) -> None:
        if not (base_code and target_code and rate):
            raise IncorrectCurrencyData
            
        if not (base_code.isalpha() and target_code.isalpha()):
            raise IncorrectInputCodeCurrency
        try:
            rate_decival = Decimal(rate)
        except (ValueError, InvalidOperation):
            raise IncorrectInputCodeCurrency("Введите число")
        
        if base_code == target_code and rate != Decimal(1):
            raise IncorrectInputCodeCurrency("Курс для одинаковых валют должен быть равен 1")

        if  rate_decival > MAX_RATE:
            raise IncorrectInputCodeCurrency(f"Курс слишком большой, введите значение до {MAX_RATE}")
        
        if  rate_decival < MIN_RATE:
            raise IncorrectInputCodeCurrency(f"Курс слишком мал, введите значение до {MIN_RATE}")
        
    def validate_convert(self, amount: str) -> Decimal:
        try:
            amount_decimal = Decimal(amount)
        except (ValueError, InvalidOperation):
            raise IncorrectInputCodeCurrency("Введите число")
        
        if amount_decimal < 0:
            raise IncorrectInputCodeCurrency("Сумма не может быть отрицательной")
        
        if amount_decimal > MAX_AMOUNT:
            raise IncorrectInputCodeCurrency(f"Сумма слишком большая, введите значение до {MAX_AMOUNT}")
        
        if amount_decimal < MIN_RATE:
            raise IncorrectInputCodeCurrency(f"Сумма слишком мала, минимальное значение {MIN_RATE}")
        
        return amount_decimal

    def _validate_profanity_words(self, text: str) -> bool:
        return any(row in text.lower() for row in self.word)
    
    def extract_currency_pair(self, pair: str) -> tuple[str, str]:
        if not pair:
            raise IncorrectInputCodeCurrency("Код валютной пары не указан")
        if len(pair) != 6:
            raise IncorrectInputCodeCurrency(f"Код валютной пары должен содержать 6 символов, получено: {len(pair)}")
        if not pair.isalpha():
            raise IncorrectInputCodeCurrency("Код валютной пары должен содержать только буквы")
        base_code : str = pair[:3]
        target_code : str = pair[3:]
        if not (base_code and target_code):
            raise IncorrectInputCodeCurrency("Пара должна состоять из 6 символов (например, USDEUR)")
        return base_code, target_code