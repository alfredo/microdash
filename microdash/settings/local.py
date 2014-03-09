import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from microdash.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*t7r%!7+0bg16e&cu*&^rw@d_i38q2$*4c^v(r3j+hr2pu6(9g'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
