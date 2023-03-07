FROM mysql:8

ENV MYSQL_DATABASE=secframework 
ENV MYSQL_ROOT_PASSWORD=root

ADD schema.sql /docker-entrypoint-initdb.de

EXPOSE 3306