"""Handler for password change."""
import logging
from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string
from django.core.exceptions import ValidationError
from django.db import transaction

from cpovc_access.models import PasswordChange, LoginAttempt

logger = logging.getLogger(__name__)


class PasswordChangePolicyHandler(object):
    """
    Runs all policies related to enforced password changes.

    Raises a ValidationError when a user is enforced to change its password
    """

    _policies = []
    policy_texts = []

    def __init__(self):
        """Class constructor."""
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_CHANGE_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

    def validate(self, user):
        """Validation method to check last password change."""
        try:
            user_pw_change = user.password_changed_timestamp
            if user_pw_change:
                user.timestamp = user_pw_change
                user.is_temporary = False
                last_pw_change = user
            else:
                last_pw_change = PasswordChange.objects.filter(
                    user=user, successful=True).order_by('-id')[0]
                if last_pw_change:
                    user.password_changed_timestamp = timezone.now()
                    user.save(update_fields=['password_changed_timestamp'])
        except IndexError:
            last_pw_change = None

        for pol in self._policies:
            pol.validate(last_pw_change)

    def update_session(self, request, user):
        """Called directly after successful authentication."""
        if not hasattr(request, 'session'):
            return

        try:
            self.validate(user)
        except ValidationError as exc:
            change_msg = unicode(exc.message)
            request.session['password_change_enforce'] = exc.code
            request.session['password_change_enforce_msg'] = change_msg
        else:
            request.session['password_change_enforce'] = False
            request.session['password_change_enforce_msg'] = None


class PasswordStrengthPolicyHandler(object):
    """
    Runs all policies related to password strength requirements.

    Raises a ValidationError when a password doesn't comply
    """

    _policies = []
    policy_texts = []

    def __init__(self):
        """Constructor for the class."""
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_STRENGTH_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

            if policy.show_policy and policy.policy_text:
                self.policy_texts.append({
                    'text': policy.policy_text,
                    'caption': policy.policy_caption,
                })

    def validate(self, password, user=None):
        """
        Validate password strength against all password policies.

        One should also provide the user (when available) that (will) use
        this password.
        Policies will raise a ValidationError when the password doesn't comply
        """
        for pol in self._policies:
            pol.validate(password, user)


class AuthenticationPolicyHandler(object):
    """
    Runs all policies related to authentication.

    Raises a ValidationError when an authentication attempt does not comply
    """

    _policies = []
    policy_texts = []

    def __init__(self):
        """Authentication constructor."""
        if self._policies:
            return

        for policy_path, kwargs in settings.AUTHENTICATION_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

    def pre_auth_checks(self, username, password, remote_addr, host):
        """Policy checks before a user is authenticated.

        No `User` instance is available yet

        Raises ValidationError for failed login attempts
        On success it returns a LoginAttempt instance

        `username` must be a string that uniquely identifies a user.
        """
        logger.info('Authentication attempt, username=%s, address=%s',
                    username, remote_addr)
        with transaction.atomic():
            username_len = LoginAttempt._meta.get_field('username').max_length
            hostname_len = LoginAttempt._meta.get_field('hostname').max_length
            attempt = LoginAttempt.objects.create(
                username=username[:username_len] if username else '-',
                source_address=remote_addr,
                hostname=host[:hostname_len],
                successful=False,
                lockout=True)
        for pol in self._policies:
            pol.pre_auth_check(attempt, password)

        return attempt

    def post_auth_checks(self, attempt):
        """Policy checks after the user has been authenticated.

        The attempt must now have a `user` instance set.

        Raises ValidationError for failed login attempts.
        """
        assert attempt.user is not None

        for pol in self._policies:
            pol.post_auth_check(attempt)

        return attempt

    def auth_success(self, attempt):
        """Run this when authentication was successful.

        i.e. after `post_auth_checks`.
        """
        logger.info(u'Authentication success, username=%s, address=%s',
                    attempt.username, attempt.source_address)

        with transaction.atomic():
            attempt.successful = True
            attempt.lockout = False
            attempt.save()

        for pol in self._policies:
            pol.auth_success(attempt)

        return attempt
