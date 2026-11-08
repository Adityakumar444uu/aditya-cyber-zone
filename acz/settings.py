import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "acz" / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

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

MEDIA_URL = '/media/'


# Use Cloudinary only when its credentials are configured.
CLOUDINARY_CONFIGURED = (
    bool(os.environ.get("CLOUDINARY_URL"))
    or all(
        os.environ.get(key)
        for key in (
            "CLOUDINARY_CLOUD_NAME",
            "CLOUDINARY_API_KEY",
            "CLOUDINARY_API_SECRET",
        )
    )
)

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.RawMediaCloudinaryStorage"
            if CLOUDINARY_CONFIGURED
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

PAYU_MERCHANT_KEY = os.environ.get("PAYU_MERCHANT_KEY", "")
PAYU_MERCHANT_SALT = os.environ.get("PAYU_MERCHANT_SALT", "")
PAYU_BASE_URL = os.environ.get(
    "PAYU_BASE_URL",
    "https://secure.payu.in/_payment"
)
PAYU_VERIFY_URL = os.environ.get(
    "PAYU_VERIFY_URL",
    "https://info.payu.in/merchant/postservice.php?form=2"
)