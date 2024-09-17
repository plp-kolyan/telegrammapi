import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from project import settings



settings.LOGGING = {
    'version': 1,
    "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}
django.setup()