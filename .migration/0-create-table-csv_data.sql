CREATE TABLE IF NOT EXISTS csv_data
(
    ticker          VARCHAR(16) NOT NULL
        PRIMARY KEY
        UNIQUE,
    company_name    VARCHAR(64) NOT NULL
        UNIQUE,
    content         TEXT DEFAULT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS csv_data_company_name_uindex
    ON csv_data (company_name);


CREATE UNIQUE INDEX IF NOT EXISTS csv_data_ticker_uindex
    ON csv_data (ticker);

