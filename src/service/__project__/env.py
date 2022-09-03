"""
Project environment management.

Configure application expected env variables' type and default values,
madiating their consuption and improving this handling

See https://django-environ.readthedocs.io/en/latest/index.html.
"""

import environ


# Define expected env variables, its casting and default value
# See https://django-environ.readthedocs.io/en/latest/tips.html.
env = environ.Env(
    ENV_FILE=(str, '.env.example'),
    SECRET_KEY=(str, None),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ['*']),
    STATIC_DIR=(str, 'static'),
)

# Manage choosen .env file consuption.
env.read_env(
    env('ENV_FILE'),
    # overwrite=True,
)

# Extra options
# env.prefix = 'DJANGO_'
# env.escape_proxy = True
