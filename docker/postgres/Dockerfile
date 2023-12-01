FROM postgres:14.10-alpine

COPY init-hive-db.sh /docker-entrypoint-initdb.d/init-hive-db.sh
COPY init_postgresql_database.sql /docker-entrypoint-initdb.d/init_postgresql_database.sql

RUN chmod +x /docker-entrypoint-initdb.d/init-hive-db.sh

EXPOSE 5432