FROM mysql:8

ENV MYSQL_DATABASE=secframework \
    MYSQL_ROOT_PASSWORD=root

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306