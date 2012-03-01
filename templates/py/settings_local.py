# -*- coding: utf-8 -*-
import logging.config
import os
import socket
import sys

DEBUG = {{debug}}
USE_DEBUG_TOOLBAR = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
     #
)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../', 'db','{{projectname}}.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_PATH,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },                 
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '{{logpath}}{{projectname}}.log',
            'formatter':'verbose',
        }, 
    },
    'loggers': {
        '': {
            'handlers':['file'],
            'propagate': False,
        },
        'django.request': {
            'handlers':['file'],
            'propagate': False,
        },
        'django': {
            'handlers':['console', 'mail_admins','file'],
            'propagate': True,
            'level':'INFO',
        },
    }
}