DELETE FROM ExchangeRates;
DELETE FROM Currencies;
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Currencies';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'ExchangeRates'