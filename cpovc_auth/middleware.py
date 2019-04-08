# -*- coding: utf-8 -*
"""Disable multiple logins middleware."""

from importlib import import_module
from django.conf import settings
from django.core.cache import cache


class UserRestrictMiddleware(object):
    """Restrict Multiple logins."""

    def process_request(self, request):
        """
        To check if different session exists for user.

        This then deletes the session data.
        """
        if request.user.is_authenticated():
            # caches = cache.get('default')
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)

            if cache_value is not None:
                if request.session.session_key != cache_value:
                    engine = import_module(settings.SESSION_ENGINE)
                    session = engine.SessionStore(session_key=cache_value)
                    session.delete()
                    cache.set(cache_key,
                              request.session.session_key,
                              cache_timeout)
            else:
                cache.set(cache_key, request.session.session_key,
                          cache_timeout)
