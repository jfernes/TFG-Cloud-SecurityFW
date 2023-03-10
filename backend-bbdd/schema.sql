CREATE SCHEMA IF NOT EXISTS secframework;
USE secframework;

CREATE TABLE IF NOT EXISTS users(
    id SMALLINT AUTO_INCREMENT,
    name TEXT,
    email varchar(50),
    password char(102),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS sslas(
    sslaid varchar(50),
    filename TEXT,
    data BLOB,
    userid SMALLINT,
    PRIMARY KEY(sslaid),
    FOREIGN KEY(userid) REFERENCES users(id)
);