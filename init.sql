USE data;

CREATE TABLE IF NOT EXISTS stock (
    timestamp DATETIME NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    price FLOAT NOT NULL,
    PRIMARY KEY (timestamp, symbol),
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp)
); 