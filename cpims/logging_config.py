from os import environ
import logging.config
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

ENV_SENTRY_DNS = 'SENTRY_LOGGING_DNS'
ENV_DEBUG = "CPIMS_DEBUG"
ENV = "APP_ENV"

APP_ENV_DEV = 'dev'
SENTRY_DNS = environ.get(ENV_SENTRY_DNS)
APP_ENV = environ.get(ENV, APP_ENV_DEV)

DEBUG = eval(environ.get(ENV_DEBUG, 'True'))

LOGGING_CONFIG = None

"""
Configure console log handlers
"""
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # root logger
        '': {
            'level': 'INFO' if DEBUG else 'ERROR',
            'handlers': ['console'],
        }
    }
})

"""
Only stream logs to sentry in a prod environment
"""
if APP_ENV != APP_ENV_DEV and SENTRY_DNS:
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.ERROR,
                event_level=logging.ERROR)
        ],
        environment=APP_ENV)
