import os

import dj_database_url

from core.env import BASE_DIR

from .base import *

SECRET_KEY = ""

DEBUG = False

ALLOWED_HOSTS = []

if bool(os.environ.get("DATABASE_URL")):
    DATABASES = {"default": dj_database_url.config()}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password reset time the number of seconds the uniquely generated uid will be valid
PASSWORD_RESET_TIMEOUT = 3600
