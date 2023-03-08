CREATE SCHEMA IF NOT EXISTS secframework;
USE secframework;

CREATE TABLE IF NOT EXISTS users(
    id BIGINT UNSIGNED AUTO_INCREMENT,
    name TEXT,
    email TEXT,
    pwdhash TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS sslas(
    id BIGINT UNSIGNED AUTO_INCREMENT,
    sslaid TEXT,
    filename TEXT,
    data BLOB,
    userid BIGINT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY(userid) REFERENCES users(id)
);