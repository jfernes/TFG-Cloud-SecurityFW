CREATE SCHEMA IF NOT EXISTS secframework;
USE secframework;

CREATE TABLE IF NOT EXISTS user(
    email varchar(50),
    name TEXT,
    password TEXT,
    PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS ssla(
    id varchar(50),
    filename TEXT,
    data LONGBLOB,
    userid varchar(50),
    PRIMARY KEY(id),
    FOREIGN KEY(userid) REFERENCES user(email)
);