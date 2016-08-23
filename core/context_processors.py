from __future__ import unicode_literals

from django.conf import settings


def app_env(request):
    """Adds app-environment to the context."""
    return {'APP_ENV': settings.APP_ENV}

