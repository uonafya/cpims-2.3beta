# CPIMS version 2.3
CPIMS v2.3
[![Build Status](https://travis-ci.org/uonafya/cpims-2.3beta.svg?branch=master)](https://travis-ci.org/uonafya/cpims-2.3beta)

### Running Tests
The project uses https://pypi.org/project/django-nose/ to run tests.

`$ pip install requirements/dev.txt` while on the root folder of the project

Then run
`$ python manage.py test --settings=cpims.test_settings`

### Docker Setup
#### Installation
Docker container setup for the app and database

`$ git clone https://github.com/uonafya/cpims-2.3beta.git && cd cpims-2.3beta`

Copy `*.sql` development database to `./docker/postgres/dbsql/`

Build the docker images-*cpims-django app* and *postgres* 

`$ docker-compose build`

Run the docker containers

`$ docker-compose up`

Run the docker container as a daemon

`$ docker-compose up -d`



