"""
Project environment management.
Configure application expected env variables' type and default values,
madiating their consuption and improving this handling.
See https://django-environ.readthedocs.io/en/latest/index.html.
"""

import environ

from django.core.management.utils import get_random_secret_key

from .path import *


__STATIC__ = 'static'


# Define expected env variables, its casting and default value
# See https://django-environ.readthedocs.io/en/latest/tips.html.
env = environ.Env(
    ENV_FILE=(str, '.env.example'),

    SECRET_KEY=(str, get_random_secret_key()),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['*']),
    INSTALLED_APPS=(list, []),

    TEMPLATE_DIRS=(list, [PROJECT_DIR / 'templates']),

    FIXTURE_DIRS=(list, [PROJECT_DIR / 'fixtures']),

    LANGUAGE_CODE=(str, 'en-US'),
    LANGUAGE_COOKIE_NAME=(str, 'django_language'),
    TIME_ZONE=(str, 'UTC'),
    USE_I18N=(bool, True),
    USE_L10N=(bool, True),
    USE_TZ=(bool, True),
    LOCALE_PATHS=(list, [PROJECT_DIR / 'locale']),

    STATIC_DIR=(str, __STATIC__),
    STATIC_URL=(str, __STATIC__ + '/'),
    STATICFILES_DIRS=(list, [PROJECT_DIR / __STATIC__]),
)

# Manage chosen .env file consumption.
env.read_env(
    env('ENV_FILE'),
    # overwrite=True,
)

# Extra options
# env.prefix = 'DJANGO_'
# env.escape_proxy = True
