# -*- coding: utf-8 -*-
import logging.config
import os
import socket
import sys

DEBUG = False
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