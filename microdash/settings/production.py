import os
import dj_database_url

from microdash.settings.base import *

env = os.getenv
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)

SECRET_KEY = env('SECRET_KEY')

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
