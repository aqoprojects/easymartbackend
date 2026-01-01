from .base import *
from pathlib import Path
import environ
import os
env = environ.Env(
  DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG=True
CORS_ALLOWED_ORIGINS = ['http://localhost:5173','http://localhost:4173']
CORS_ALLOW_CREDENTIALS = True 

DATABASES = {'default': env.db()}


STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media'


EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CELERY_BROKER_URL = env('RABBITMQ_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPTED_CONTENT = env.list('CELERY_ACCEPTED_CONTENT')
CELERY_RESULT_SERIALIZER = env('CELERY_RESULT_SERIALIZER')
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER')
CELERY_TIMEZONE = env('CELERY_TIMEZONE')


STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
WEBHOOK_SECRET = env("WEBHOOK_SECRET")


CHANNEL_LAYERS = {
  "default": {
      "BACKEND": "channels_redis.core.RedisChannelLayer",
      "CONFIG": {
          "hosts": [env("CHANNEL_LAYERS_REDIS")],
      },
  },
}