"""Policies for password change."""
import datetime
import hashlib

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cpovc_access import BasePolicy


class PasswordChangePolicy(BasePolicy):
    """Policies that require a user to change its password.

    `change_password` which raises a ValidationError when a user is
    enforced to change its password. Returns None otherwise
    """

    def validate(self, last_pw_change):
        """Method is not implemented."""
        raise NotImplemented()


class PasswordChangeExpired(PasswordChangePolicy):
    """Enforces expired password to be changed."""

    max_age = 90
    policy_text = _('One is required to change passwords every {age} days.')
    text = _('Your password has expired and must be changed.')
    allow_empty_password_history = False

    def validate(self, last_pw_change):
        """Validate password change for expired passwords."""
        if last_pw_change is None:
            # Enforce a password change when user has no PasswordChange
            # This will happen when introducing Django auth policy or for
            # new users
            if not self.allow_empty_password_history:
                raise ValidationError(self.text, code='password-expired')
            else:
                return

        expire_at = (last_pw_change.timestamp +
                     datetime.timedelta(days=self.max_age))

        if timezone.now() > expire_at:
            raise ValidationError(self.text, code='password-expired')


class PasswordChangeTemporary(PasswordChangePolicy):
    """Enforces temporary passwords to be changed."""

    text = _('Your must change your temporary password into a '
             'personal password.')

    def validate(self, last_pw_change):
        """Password validation with temp."""
        if last_pw_change is not None and last_pw_change.is_temporary:
            raise ValidationError(self.text, code='password-temporary')


def update_password(session, user):
    """Store hashed version of users' password hash in the current session."""
    hd = hashlib.sha256('pwch' + user.password).hexdigest()
    session['password_hash'] = hd


def password_changed(session, user):
    """
    Check if password changed during session.

    without updating the password stored in the session.
    """
    if not user.is_authenticated():
        return False

    if not user.has_usable_password():
        return False

    if 'password_hash' not in session:
        update_password(session, user)
        return False

    hd = hashlib.sha256('pwch' + user.password).hexdigest()
    return session.get('password_hash', '') != hd
