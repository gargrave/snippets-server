from .base import *

DEBUG = True
BUILD = 'dev'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snippets2_local',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 500
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
)

# for dev builds, read the secret key from file
with open('etc/dev_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

mailgun_api = ''
with open('etc/mailgun_api.txt') as f:
    mailgun_api = f.read().strip()

mailgun_domain = ''
with open('etc/mailgun_domain.txt') as f:
    mailgun_domain = f.read().strip()

ANYMAIL = {
    "MAILGUN_API_KEY": mailgun_api,
    "MAILGUN_SENDER_DOMAIN": mailgun_domain,
}
