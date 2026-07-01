import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lmq-*5^5*$4+9$#c4e^yd0eanw@!wck0ddo@re@&jcquxv#1xb'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customers_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'acz.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True

JAZZMIN_SETTINGS = {
    "site_title": "Aditya Cyber Zone",
    "site_header": "Aditya Cyber Zone",
    "site_brand": "Aditya Cyber Zone",
    "welcome_sign": "Welcome to Aditya Cyber Zone Dashboard",
    "copyright": "Aditya Cyber Zone",

    "show_recent_actions": True,

    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "Customers", "url": "/admin/customers_app/customer/"},
        {"name": "Applications", "url": "/admin/customers_app/application/"},
        {"name": "Check Status", "url": "/check-status/"},
        {"name": "Dashboard Count", "url": "/customers/"},
    ],

    "icons": {
        "customers_app.Customer": "fas fa-users",
        "customers_app.Application": "fas fa-file-alt",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "flatly",
    "navbar": "navbar-info navbar-light",
    "accent": "accent-purple",
    "sidebar": "sidebar-light-info",
    "brand_colour": "navbar-info",

    "button_classes": {
        "primary": "btn-info",
        "secondary": "btn-secondary",
        "info": "btn-primary",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

RAZORPAY_KEY_ID = os.environ.get("rzp_live_T8HGoswPNJPpZH")
RAZORPAY_KEY_SECRET = os.environ.get("FLIFqomvrbakoDjyGbC8T0N3")
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")