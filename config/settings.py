# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True,
ROOT_URLCONF = 'config.urls'
SECRET_KEY = 'ajlafilip'
JWT_KEY = 'qweqeqewqeqeqewq'
JWT_EXPIRE = 900 # 15 mins
WSGI_APPLICATION = 'config.wsgi.application'

INSTALLED_APPS = (
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # third party apps
    'rest_framework',
    # local apps
    'api',
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
