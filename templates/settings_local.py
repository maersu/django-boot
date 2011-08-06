# -*- coding: utf-8 -*-
import logging.config
import os
import socket
import sys

DEBUG = True

USE_DEBUG_TOOLBAR = True

INTERNAL_IPS = ('127.0.0.1', socket.gethostbyname('app.dev'))

ADMINS = (
     #
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',             # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../../db/{{projectname}}.db',       # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
DEBUG = True
USE_DEBUG_TOOLBAR = False
