from .base import * #noqa
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="b7J4B928Ps8d8PGDMEtCktk2VQJK9SPik-IDF4g8dLX9K9bs-As",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@apiimperfect.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "Authors Haven"