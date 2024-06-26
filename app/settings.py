import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY =  os.environ.get('SECRET_KEY', 'django-insecure-u8v812cu1-%l^esusdydqbya2=((uv2%bsouae=))fmf3q04(v')
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'countpesa-server-hptwt6zxga-bq.a.run.app',
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://countpesa.web.app",
    "http://localhost:4200",
    "http://localhost:3000",
]

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'django_q',
    'parser',
    'feedback'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

# Database only used to enable django_q to run asynchronous tasks ie posting feedback to g-sheets
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

Q_CLUSTER = {
    "name": "api-v2",
    "orm": "default",
    "ack_failures": True,
    'timeout': 500,
    'retry': 600,
    'max_attempts': 1,
    'attempt_count': 1
}
