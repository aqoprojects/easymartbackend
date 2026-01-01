from .base import *
from pathlib import Path
import environ
import os 
env = environ.Env(
  DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


DATABASES = {'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': '/tmp/db.sqlite3',
  }
}


STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media'

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True 

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPTED_CONTENT = env.list('CELERY_ACCEPTED_CONTENT')
CELERY_RESULT_SERIALIZER = env('CELERY_RESULT_SERIALIZER')
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER')
CELERY_TIMEZONE = env('CELERY_TIMEZONE')
CELERY_BROKER_USE_SSL = True  
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
WEBHOOK_SECRET = env("WEBHOOK_SECRET")


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'accounts.authentication.CookieJWTAuthentication',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,  # Rotate on refresh (best practice)
    'BLACKLIST_AFTER_ROTATION': True,  # Auto-blacklist old refresh tokens
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env("SECRET_KEY"),  # Use env var in prod
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),  # Not used since we're using cookies
    'USER_ID_FIELD': 'customer_id',  # Custom PK field
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
   
}
