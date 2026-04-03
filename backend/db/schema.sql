PRAGMA foreign_keys = ON;

CREATE TABLE Currencies (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code VARCHAR NOT NULL UNIQUE,
    FullName VARCHAR NOT NULL,
    Sign VARCHAR NOT NULL
);

CREATE TABLE ExchangeRates (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BaseCurrencyId INT NOT NULL,
    TargetCurrencyId INT NOT NULL,
    Rate DECIMAL(6) NOT NULL CHECK(Rate > 0),
    FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies(ID),
    FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies(ID),
    UNIQUE(BaseCurrencyId, TargetCurrencyId)
)