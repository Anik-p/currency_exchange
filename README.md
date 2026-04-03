# Currency Exchange API

##  Описание

REST API для управления валютами, курсами обмена и конвертации валют.

Проект создан в рамках Python Roadmap Сергея Жукова ->

https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/

Основной функционал:

* регистрация валют
* добавление и обновление курсов обмена
* получение списка валют и курсов
* конвертацию валют
* поддержка cross-rate через USD

---

##  Архитектура

Проект реализован по слоистой архитектуре:

```
Controller → Service → DAO → Database
```

##  Структура проекта

* project/
* controllers   - обработка HTTP-запросов
* services      - бизнес-логика
* dao           - работа с БД
* dto           - структуры данных
* handler       - HTTP server, router
* db            - SQL и инициализация БД
* config        - конфигурация
* utils         - вспомогательные функции

* run.py         - точка входа
* server_app.py  - запуск HTTP сервера
---

##  Запуск проекта

###  Требования

* Python 3.10+
* SQLite3 (встроен Python)

### 1. Клонирование

```bash
git clone <repo_url>
cd project
```

### 2. Запуск

```bash
python run.py
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

###   Получение списка валют

```
GET /currencies
```
Пример ответа:
```
[

{
    "id": 1,
    "name": "United States dollar",
    "code": "USD",
    "sign": "$"
}

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

```
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

```
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

```
[
    {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },   
    {
        "id": 0,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
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
Ответ:

```
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

```
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

```
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

```
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
## Ошибки

Все ошибки возвращают в формате:

{
    "message: "описание ошибки"
}