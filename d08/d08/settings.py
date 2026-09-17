"""
Django settings for the d08 project.

Secrets are never hardcoded here: they are read from a local .env file that
.gitignore excludes, as required by Chapter I of the subject.
"""

from pathlib import Path

import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load BASE_DIR/.env into the environment. Nothing in this file falls back to a
# hardcoded credential: a missing .env is a loud error, not a silent default.
load_dotenv(BASE_DIR / ".env")


def env(name, default=None):
    """Read an environment variable, or fail with actionable instructions."""
    value = os.environ.get(name, default)
    if value is None:
        raise ImproperlyConfigured(
            f"Missing environment variable {name!r}. "
            f"Copy {BASE_DIR / '.env.example'} to {BASE_DIR / '.env'} "
            f"and set a value. See README.md."
        )
    return value


SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes", "on")

# Comma-separated. A VM reached from the host on its own IP sends that IP as
# the Host header, so it has to be listed or Django answers 400.
ALLOWED_HOSTS = [
    host.strip()
    for host in env("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]


INSTALLED_APPS = [
    # Daphne replaces the WSGI runserver with an ASGI one so that `runserver`
    # can serve the WebSocket routes of ex01-ex04. It must come first.
    "daphne",
    # The subject requires the default administration application to be kept.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "account",
    "chat",
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

ROOT_URLCONF = "d08.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI is kept for completeness; ASGI is what actually serves the project.
WSGI_APPLICATION = "d08.wsgi.application"
ASGI_APPLICATION = "d08.asgi.application"

# The in-memory layer needs no external service, which keeps the project
# runnable with nothing but `pip install -r requirements.txt`. It is scoped to
# a single process, which is exactly what `runserver` gives us.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Overridable because sqlite misbehaves on a VirtualBox shared folder
# (vboxsf does not implement POSIX locking), so inside a VM the database is
# better placed on the guest filesystem than on the share.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env("DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The chat is for logged-in users only (ex01); unauthenticated visitors are
# sent to the AJAX login page built in ex00.
LOGIN_URL = "/account"
LOGIN_REDIRECT_URL = "/account"

# Number of past messages replayed to a user joining a room (ex02).
CHAT_HISTORY_SIZE = 3
