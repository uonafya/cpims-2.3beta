"""Extended settings for password policies."""
from django.conf import settings

# django_auth_policy replaces the default Django auth UserAdmin to enforce
# authentication policies on the admin interface. Set this to False when
# django_auth_policy shouldn't replace UserAdmin.
REPLACE_AUTH_USER_ADMIN = getattr(settings, 'REPLACE_AUTH_USER_ADMIN', True)

# django_auth_policy uses view names to resolve the correct (enforced)
# login, logout, and password_change views.
PASSWORD_CHANGE_VIEW_NAME = getattr(
    settings, 'ENFORCED_PASSWORD_CHANGE_VIEW_NAME', 'password_change')
LOGIN_VIEW_NAME = getattr(settings, 'LOGIN_VIEW_NAME', 'login')
LOGOUT_VIEW_NAME = getattr(settings, 'LOGOUT_VIEW_NAME', 'logout')

# Set this to the list of public urls that are excluded from global
# authentication when using LoginRequiredMiddleware.
PUBLIC_URLS = getattr(settings, 'PUBLIC_URLS', [])

# Set this to the desired length of django_auth_policy generated temporary
# passwords.
TEMP_PASSWORD_LENGTH = getattr(settings, 'TEMP_PASSWORD_LENGTH', 12)

# Set this to the desired character set of django_auth_policy generated
# temporary passwords.
TEMP_PASSWORD_CHARS = getattr(settings, 'TEMP_PASSWORD_CHARS',
                              'abcdefghijlkmnopqrstuvwxyz'
                              'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                              '0123456789')

# django_auth_policy automatically logs users out of all sessions after a
# password change by default. Set this to False to disable automatic logouts.
LOGOUT_AFTER_PASSWORD_CHANGE = getattr(settings,
                                       'LOGOUT_AFTER_PASSWORD_CHANGE', True)


# Attribute put onto views by the login_not_required decorator.
LOGIN_NOT_REQUIRED_MARKER = getattr(settings,
                                    'LOGIN_NOT_REQUIRED_MARKER',
                                    'cpovc_access__login_not_required')
