# -*- coding: utf-8 -*-
<<<<<<< HEAD
=======
import logging.config
import os
import socket
import sys

DEBUG = True

USE_DEBUG_TOOLBAR = True

INTERNAL_IPS = ('127.0.0.1', socket.gethostbyname('app.dev'))
>>>>>>> 4f28f8732355d4543052dbedf6c5de8bdf306318

ADMINS = (
     #
)

DATABASES = {
    'default': {
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../../db/{{projectname}}.db',                      # Or path to database file if using sqlite3.
=======
        'ENGINE': 'django.db.backends.sqlite3',             # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../../db/{{projectname}}.db',       # Or path to database file if using sqlite3.
>>>>>>> 4f28f8732355d4543052dbedf6c5de8bdf306318
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
DEBUG = True
<<<<<<< HEAD
USE_DEBUG_TOOLBAR = True
TEMPLATE_DEBUG = DEBUG

=======
USE_DEBUG_TOOLBAR = False
>>>>>>> 4f28f8732355d4543052dbedf6c5de8bdf306318
