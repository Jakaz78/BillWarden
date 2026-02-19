"""
Django settings for BillWarden project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "10.0.2.2",  # Dla emulatora Androida
]

# 4. Aplikacje
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # Twoja aplikacja
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "BillWarden.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],  # Upewnienie się co do ścieżki
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "BillWarden.wsgi.application"

# 5. Baza Danych
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 6. Walidacja haseł
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 7. Lokalizacja i Czas
LANGUAGE_CODE = "pl-pl"  # Małe litery to standard

# Zmieniamy na Polskę, żeby godziny na paragonach zgadzały się z rzeczywistością
TIME_ZONE = "Europe/Warsaw"

USE_I18N = True
USE_TZ = True

# 8. Pliki Statyczne (CSS, JS, Ikony)
STATIC_URL = "static/"


# 9. Pliki Media (Zdjęcia paragonów)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Ustawienia domyślne dla kluczy głównych (ważne w nowszym Django)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
