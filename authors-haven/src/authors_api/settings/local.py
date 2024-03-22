from .base import * #noqa
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="b7J4B928Ps8d8PGDMEtCktk2VQJK9SPik-IDF4g8dLX9K9bs-As",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]