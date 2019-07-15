"""
Django settings for cpims project.

Generated by 'django-admin startproject' using Django 1.8.4.
"""
import os

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': cpims_db_instance,
        'USER': cpims_db_user,
        'PASSWORD': cpims_db_pass,
        'HOST': cpims_db_host,
        'PORT': cpims_db_port,
    }
}

if os.environ.get('TRAVIS'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=cpovc_auth,cpovc_registry,cpovc_main,cpovc_forms,cpovc_gis,cpovc_settings,crispy_forms,cpovc_ovc,import_export',
    '--cover-html',
]
DEBUG = False
