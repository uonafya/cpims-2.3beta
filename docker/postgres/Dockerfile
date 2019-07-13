FROM postgres:10.9-alpine
COPY ./docker/postgres/dbsql/*.sql /docker-entrypoint-initdb.d/
RUN chmod a+r /docker-entrypoint-initdb.d/*
