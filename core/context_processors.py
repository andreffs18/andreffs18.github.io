from __future__ import unicode_literals

from django.conf import settings
from datetime import datetime


def app_env(request):
    """Adds app-environment to the context."""
    return {'APP_ENV': settings.APP_ENV}


def my_age(request):
    """Adds app-environment to the context."""
    return {'my_age': datetime.now().year - 1993}

