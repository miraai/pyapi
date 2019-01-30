# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True,
ROOT_URLCONF = 'config.urls'
SECRET_KEY = 'topappsecret'
WSGI_APPLICATION = 'config.wsgi.application'
# JWT Config
JWT_KEY = 'topjwtsecret'
JWT_EXPIRE = 900 # 15 mins
# Committing to pushing secrets
# Email hunter
EMAIL_HUNTER_BASE_URL = 'https://api.hunter.io/v2/'
EMAIL_HUNTER_API_KEY = '13d09295500e119264cf6046778df4853b61c997'
# ClearBit Enrichment
CLEARBIT_BASE_URL = 'https://person.clearbit.com/v2/'
CLEARBIT_API_KEY = 'sk_785aa1025b1ba132fbeeca04c1cb2acb'
INSTALLED_APPS = (
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # third party apps
    'rest_framework',
    # local apps
    'api',
)

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
