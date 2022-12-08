CREATE TABLE app_user
(
    id            BIGINT         NOT NULL
        PRIMARY KEY
        UNIQUE,
    username      VARCHAR(32)    NOT NULL
        UNIQUE,
    email         VARCHAR(64)    NOT NULL
        UNIQUE,
    password_hash CHAR(66)       NOT NULL,
    rank          SMALLINT       NOT NULL
        DEFAULT 0
);

CREATE UNIQUE INDEX app_user_id_uindex
    ON app_user (id);

CREATE UNIQUE INDEX app_user_username_uindex
    ON app_user (username);

CREATE UNIQUE INDEX app_user_email_uindex
    ON app_user (email);
