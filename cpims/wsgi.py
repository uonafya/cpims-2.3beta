"""
WSGI config for cpims project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

sys.path.append('/opt/cpims')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cpims.settings")

application = get_wsgi_application()
