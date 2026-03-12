"""
Django settings for kanmind project.

KanMind backend configuration:
- installed apps
- middleware
- database
- auth
- CORS
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present (safe for fresh clones)
load_dotenv(BASE_DIR / ".env")


# ---------------------------
# Security
# ---------------------------

# Fallback key for local dev so the project runs after clone
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

DEBUG = os.getenv("DEBUG", "1") == "1"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,.onrender.com"
).split(",")

# ---------------------------
# Applications
# ---------------------------

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "authentication",
    "tasks",
    "boards",
]


# ---------------------------
# Middleware
# ---------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kanmind.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "kanmind.wsgi.application"


# ---------------------------
# Database (default: SQLite)
# ---------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("SQLITE_NAME", "db.sqlite3"),
    }
}


# ---------------------------
# Password validation
# ---------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------
# i18n
# ---------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ---------------------------
# Static files
# ---------------------------

STATIC_URL = "static/"


# ---------------------------
# CORS
# ---------------------------

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500,https://mya63.github.io"
).split(",")
CORS_ALLOW_CREDENTIALS = True


# ---------------------------
# DRF
# ---------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}