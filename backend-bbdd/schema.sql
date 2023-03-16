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

CREATE TABLE IF NOT EXISTS intent(
    id varchar(80),
    sslaid varchar(50),
    name TEXT,
    description TEXT,
    PRIMARY KEY (id, sslaid),
    FOREIGN KEY (sslaid) REFERENCES ssla(id) ON DELETE CASCADE
);

-- CREATE TABLE IF NOT EXISTS seccontrol();