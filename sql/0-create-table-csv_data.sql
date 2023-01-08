CREATE TABLE IF NOT EXISTS csv_data
(
    symbol          VARCHAR(16) NOT NULL
        PRIMARY KEY
        UNIQUE,
    content         TEXT DEFAULT NULL
);


CREATE UNIQUE INDEX IF NOT EXISTS stock_record_id_uindex
    ON csv_data (symbol);

