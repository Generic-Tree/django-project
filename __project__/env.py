"""
Project environment management.
Configure application expected env variables' type and default values,
madiating their consuption and improving this handling.
See https://django-environ.readthedocs.io/en/latest/index.html.
"""

import environ

from django.core.management.utils import get_random_secret_key

from .path import *


# Define expected env variables, its casting and default value
# See https://django-environ.readthedocs.io/en/latest/tips.html.
env = environ.Env(
    ENV_FILE=(str, '.env.example'),

    SECRET_KEY=(str, get_random_secret_key()),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['*']),
    FIXTURE_DIRS=(list, [PROJECT_DIR / 'fixtures'])
)

# Manage chosen .env file consumption.
env.read_env(
    env('ENV_FILE'),
    # overwrite=True,
)

# Extra options
# env.prefix = 'DJANGO_'
# env.escape_proxy = True
