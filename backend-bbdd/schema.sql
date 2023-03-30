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

CREATE TABLE IF NOT EXISTS contract(
    contractid varchar(50),
    providerid varchar(50),
    consumerid varchar(50),
    filename TEXT,
    data LONGBLOB,
    PRIMARY KEY (contractid, providerid, consumerid),
    FOREIGN KEY (consumerid) REFERENCES user(email) ON DELETE CASCADE,
    FOREIGN KEY (providerid) REFERENCES user(email) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS seccontrol(
    id varchar(100),
    name varchar(100),
    control_domain varchar(10),
    description TEXT,
    intentid varchar(80),
    PRIMARY KEY (id, intentid),
    FOREIGN KEY (intentid) REFERENCES intent(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admin(
    id varchar(50),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES user(email) ON DELETE CASCADE
);

INSERT INTO user(email, name, password) VALUES("admin@um.es", "admin", "admin");

INSERT INTO admin(id) VALUES ("admin@um.es");

INSERT INTO user(email, name, password) VALUES("dsevilla@um.es", "admin", "admin");

INSERT INTO user(email, name, password) VALUES("julian@um.es", "admin", "admin");




