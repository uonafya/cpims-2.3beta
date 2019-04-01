"""This is for handling all authentication checks."""
import logging
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cpovc_access import signals
from cpovc_access import BasePolicy

logger = logging.getLogger(__name__)


class AuthenticationPolicy(BasePolicy):
    """Checks run when authenticating.

    Policies can define:
    `pre_auth_check` for checks that should be run before attempting to
    authenticate provided credentials.

    `post_auth_check` for checks that should be run after attempting to
    authenticate provided credentials.

    Both `pre_auth_check` and `post_auth_check` raise a ValidationError
    when authentication fails to comply with the policy

    `auth_success` is run when the attempt was successful and should not
    raise a ValidationError
    """

    def pre_auth_check(self, loginattempt, password):
        """Pre auth check."""
        pass

    def post_auth_check(self, loginattempt):
        """Post auth checks."""
        pass

    def auth_success(self, loginattempt):
        """Success check."""
        pass


class AuthenticationBasicChecks(AuthenticationPolicy):
    """Handle basich checks."""

    text = _("Please enter a correct username and password. "
             "Note that both fields may be case-sensitive.")

    def pre_auth_check(self, loginattempt, password):
        """Pre check."""
        if not loginattempt.username:
            logger.info(u'Authentication failure, address=%s, '
                        'no username supplied.',
                        loginattempt.source_address)
            raise ValidationError(self.text, code='invalid_login')

        if not password:
            logger.info(u'Authentication failure, username=%s, '
                        'address=%s, no password supplied.',
                        loginattempt.username,
                        loginattempt.source_address)
            raise ValidationError(self.text, code='invalid_login')

    def post_auth_check(self, loginattempt):
        """Post login check."""
        if loginattempt.user is None:
            logger.info(u'Authentication failure, username=%s, '
                        'address=%s, invalid authentication.',
                        loginattempt.username, loginattempt.source_address)
            raise ValidationError(self.text, code='invalid_login')

        if not loginattempt.user.is_active:
            logger.info(u'Authentication failure, username=%s, '
                        'address=%s, user inactive.',
                        loginattempt.username, loginattempt.source_address)
            raise ValidationError(self.text, code='inactive')


class AuthenticationDisableExpiredUsers(AuthenticationPolicy):
    """Disable ALL users that have been expired.

    Users must have an `is_active` and a `last_login` field

    Reactivate user by setting is_active to True and last_login to
    now.
    """

    # Days after which users without a successful login expire, make sure
    # user sessions are short enough to enforce frequent re-logins
    inactive_period = 90

    def pre_auth_check(self, loginattempt, password):
        """Precheck function."""
        expire_at = timezone.now() - datetime.timedelta(
            days=self.inactive_period)

        expired = get_user_model().objects.filter(is_active=True,
                                                  last_login__lt=expire_at)

        for user in expired:
            logger.info(u'User %s disabled because last login was at %s',
                        unicode(user), user.last_login)
            # Send signal to be used to alert admins
            signals.user_expired.send(sender=user, user=user)

        expired.update(is_active=False)
