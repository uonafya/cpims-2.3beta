"""Middleware to handle logins checks."""
import logging

from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import resolve, reverse
from django.views.decorators.csrf import requires_csrf_token

from cpovc_access.handlers import PasswordChangePolicyHandler
from cpovc_access.forms import StrictPasswordChangeForm
from cpovc_access.password_change import update_password, password_changed
from cpovc_access.decorators import watch_login
from cpovc_access.settings import (
    LOGIN_VIEW_NAME,
    LOGOUT_AFTER_PASSWORD_CHANGE,
    LOGOUT_VIEW_NAME,
    PASSWORD_CHANGE_VIEW_NAME,
)

logger = logging.getLogger(__name__)


class FailedLoginMiddleware(object):
    """Handle failed logins."""

    def __init__(self, *args, **kwargs):
        """Handle failure constructor."""
        super(FailedLoginMiddleware, self).__init__(*args, **kwargs)

        # watch the auth login
        auth_views.login = watch_login(auth_views.login)


class ViewDecoratorMiddleware(object):
    """
    When this middleware is installed, by default it watches.

    the django.auth.views.login.

    This middleware allows adding protection to other views without the need
    to change any urls or dectorate them manually.

    Add this middleware to your MIDDLEWARE settings after
    `axes.middleware.FailedLoginMiddleware` and before the django
    flatpages middleware.
    """

    watched_logins = getattr(
        settings, 'AXES_PROTECTED_LOGINS', (
            '/accounts/login/',
        )
    )

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Method to process the view."""
        if request.path in self.watched_logins:
            return watch_login(view_func)(request, *view_args, **view_kwargs)

        return None


class AuthenticationPolicyMiddleware(object):
    """This middleware enforces the following policy.

    - Change of password when password has expired;
    - Change of password when user has a temporary password;
    - Logout disabled users;

    This is enforced using middleware to prevent users from accessing any page
    handled by Django without the policy being enforced.
    """

    change_password_path = reverse(PASSWORD_CHANGE_VIEW_NAME)
    login_path = reverse(LOGIN_VIEW_NAME)
    logout_path = reverse(LOGOUT_VIEW_NAME)

    password_change_policy_handler = PasswordChangePolicyHandler()

    def process_request(self, request):
        """Method to handle requests."""
        assert hasattr(request, 'user'), (
            'AuthenticationPolicyMiddleware needs a user attribute on '
            'request, add AuthenticationMiddleware before '
            'AuthenticationPolicyMiddleware in MIDDLEWARE_CLASSES')

        # This middleware does nothing for unauthenticated users
        if not request.user.is_authenticated():
            return None

        # Check if users' password has been changed, and then logout user.
        # To prevent logout at password change views call the
        # `update_password` function in that view
        if 'password_hash' not in request.session:
            update_password(request.session, request.user)

        # Log out disabled users
        if not request.user.is_active:
            logger.info('Log out inactive user, user=%s', request.user)
            return self.logout(request)

        # Do not do password change for certain URLs
        if request.path in (self.change_password_path, self.login_path,
                            self.logout_path):
            return None

        # Check for 'enforce_password_change' in session set by login view
        if request.session.get('password_change_enforce', False):
            return self.password_change(request)

        return None

    def process_response(self, request, response):
        """Method to handle response."""
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            return response

        # When password change is enforced, check if this is still required
        # for next request
        if request.session.get('password_change_enforce', False):
            self.password_change_policy_handler.update_session(
                request, request.user)

        # Check if users' password has been changed, and then logout user.
        # To prevent logout at password change views call the
        # `update_password` function in that view
        # Ignore non 2xx responses (e.g. redirects).
        if (response.status_code >= 200 and
                response.status_code < 300 and
                LOGOUT_AFTER_PASSWORD_CHANGE and
                password_changed(request.session, request.user)):
            # Update password change time
            user = request.user
            user.password_changed_timestamp = timezone.now()
            user.save(update_fields=['password_changed_timestamp'])

            logger.info('Logout session because user changed its password')
            request.session['password_change_relogin'] = True
            return self.logout(request)

        return response

    def password_change(self, request):
        """Return 'password_change' view.

        This resolves the view with the name 'password_change'.
        Overwrite this method when needed.
        """
        view_func, args, kwargs = resolve(self.change_password_path)

        if 'password_change_form' in kwargs:
            """Check if been flagged."""
            assert issubclass(kwargs['password_change_form'],
                              StrictPasswordChangeForm), (
                "Use cpovc_access StrictPasswordChangeForm for password "
                "changes.")

        # Provide extra context to be used in the password_change template
        if 'extra_context' in kwargs:
            kwargs['extra_context']['password_change_enforce'] = \
                request.session.get('password_change_enforce')
            kwargs['extra_context']['password_change_enforce_msg'] = \
                request.session.get('password_change_enforce_msg')

        # Run 'requires_csrf_token' because CSRF middleware might have been
        # skipped over here
        resp = requires_csrf_token(view_func)(request, *args, **kwargs)
        update_password(request.session, request.user)
        return resp

    def logout(self, request):
        """Logout method."""
        messages.info(request, 'Please relogin')
        view_func, args, kwargs = resolve(self.logout_path)
        return view_func(request, *args, **kwargs)
