# Currency Exchange

##  Описание

REST API для управления валютами, курсами обмена и конвертации валют.

Проект создан в рамках Python Roadmap Сергея Жукова -> https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/

Основной функционал:

* регистрация валют
* добавление и обновление курсов обмена
* получение списка валют и курсов
* конвертацию валют
* поддержка cross-rate через USD

Деплой: http://195.209.212.50

---

##  Архитектура

Проект реализован по слоистой архитектуре (Layered Architecture):

```
Controller → Service → DAO → Database
```

##  Структура проекта

currency_exchange/

- controllers/   - обработка HTTP-запросов
- services/      - бизнес-логика
- dao/           - работа с БД
- dto/           - структуры данных
- handler/       - HTTP server, router
- db/            - SQL и инициализация БД
- config/        - конфигурация
- utils/         - вспомогательные функции

- run.py         - точка входа
- server_app.py  - запуск HTTP сервера

---

##  Запуск локального проекта

###  Требования

* Python 3.10+
* SQLite3 (встроен Python)

### 1. Клонирование

```bash
git clone https://github.com/Anik-p/currency_exchange.git
```

### 2. Настройка конфигурации

В backend/config/base_config измените следующие параметры:

```python
HOST = "localhost"  # Для локального запуска
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "exchange.db"
```

Так же в fronted/js/app.js измените строку const host на:

```js
const host = "http://localhost:8000"
```

### 3. Запуск

Запуск Backend:
```bash
python run.py
```

Запуск Frontend:

Через Docker:
```bash
cd frontend
chmod +x launch-local-nginx.sh
./launch-local-nginx.sh
```

Через браузер:
```bash
index.html
```

* Автоматически создается база данных
* Выполняется инициализация (schema + seed).

---

## База данных

Используется SQLite.

Инициализация выполняется через:

* schema.sql — структура таблиц
* seed.sql — базовые валюты
* rate.sql — начальные курсы
---

## Frontend

Для работы с API используется готовый frontend:

[currency-exchange-frontend](https://github.com/zhukovsd/currency-exchange-frontend)

* готовый пользовательский интерфейс для работы с API
* поддержка:
    * просмотра валют
    * работы с курсами
    * конвертации
* взаимодействует с backend через HTTP-запросы

---

##  API

### Ошибки

Все ошибки возвращают в формате:

```
{
    "message: "описание ошибки"
}
```

###   Получение списка валют

```
GET /currencies
```

Пример ответа:

```json
[

{
    "id": 1,
    "name": "United States dollar",
    "code": "USD",
    "sign": "$"
}, 

...

]
```
---

###  Получение конкретной валюты

```
GET /currency/{code}
```

Пример:

```
GET /currency/USD
```

Пример ответа:

```json
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```
---

###  Добавление новой валюты в базу

```
POST /currencies
```

Content-Type: application/x-www-form-urlencoded

Пример тела запроса: 

```
name=Euro&code=EUR&sign=€
```

Пример ответа:

```json
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```

---

###  Получение списка всех обменных курсов

```
GET /exchangeRates
```

```json
[
    {
        "id": 1,
        "baseCurrency": {
            "id": 1,
            "name": "United States dollar",
            "code": "USD",
            "sign": "$"
        },
        "targetCurrency": {
            "id": 2,
            "name": "Euro",
            "code": "EUR",
            "sign": "€"
        },
        "rate": "0.92"
    },

    ...
]
```
---

###  Получение конкретного обменного курса

```
GET /exchangeRate/{pair}
```

Пример:

```
GET /exchangeRate/USDEUR
```

Пример ответа:

```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```

---

###  Добавление нового обменного курса в базу

```
POST /exchangeRates
```

Ответ:

```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```

---

###  Обновление существующего в базе обменного курса

```
PATCH /exchangeRate/{pair}
```

Пример ответа:

```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```

---

###  Конвертация

```
GET /convert?from=USD&to=EUR&amount=100
```
Пример ответа:

```json
{
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Australian dollar",
        "code": "AUD",
        "sign": "A€"
    },
    "rate": 1.45,
    "amount": 10.00,
    "convertedAmount": 14.50
}
```