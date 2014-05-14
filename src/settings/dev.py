### dev.py
from common import *
DEBUG = True

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

