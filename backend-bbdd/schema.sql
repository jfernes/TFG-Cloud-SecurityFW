CREATE SCHEMA IF NOT EXISTS secframework;
USE secframework;

CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    email varchar(50),
    pwdhash TEXT,
    PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS sslas(
    sslaid varchar(50),
    filename TEXT,
    data BLOB,
    userid varchar(50),
    PRIMARY KEY(sslaid),
    FOREIGN KEY(userid) REFERENCES users(email)
);