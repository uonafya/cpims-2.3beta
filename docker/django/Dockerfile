FROM python:2.7

ENV PYTHONUNBUFFERED 1

# RUN apt update \
#   # psycopg2 dependencies
#   # && apt add --virtual build-deps gcc python2-dev musl-dev \
#   # && apk add postgresql-dev \
#   # Pillow dependencies
#   && apt add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
#   # CFFI dependencies
#   && apt add libffi-dev py-cffi \
#   # Translations dependencies
#   && apt add gettext \
#   # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
#   && apt add postgresql-client

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

COPY ./docker/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


# Creating working directory
RUN mkdir /app
WORKDIR /app

# Copying requirements
COPY . ./app

# CMD setup

ENTRYPOINT ["/entrypoint"]
