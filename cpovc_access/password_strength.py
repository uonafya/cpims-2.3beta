"""Handle password rules."""
import re
import unicodedata

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cpovc_access import BasePolicy
from cpovc_access.models import PasswordChange


def _normalize_unicode(value):
    try:
        value = unicodedata.normalize('NFKD', unicode(value))
        return value.encode('ascii', 'ignore').strip().lower()
    except UnicodeDecodeError:
        return value


class PasswordStrengthPolicy(BasePolicy):
    """Password strength policy classes must implement.

    `validate` a method which accept a password and the related user and raises
    a validation error when the password doesn't validate the policy.

    Optionally:

    `policy_text` a property which returns a short text to be displayed in
    password policy explenations

    `policy_caption` a property which returns a short caption to be displayed
    with the password policy.
    """

    show_policy = True

    def validate(self, value, user=None):
        """Validation text."""
        raise NotImplemented()

    @property
    def policy_text(self):
        """Some policy text."""
        return None

    @property
    def policy_caption(self):
        """Policy caption."""
        return None


class PasswordMinLength(PasswordStrengthPolicy):
    """Class for minimum length password."""

    min_length = 8
    text = _('Passwords must be at least {min_length} characters in length.')

    def validate(self, value, user=None):
        """Method to validate min pass length."""
        if self.min_length is None:
            return

        if len(value) < self.min_length:
            msg = self.text.format(min_length=self.min_length)
            raise ValidationError(msg, code='password_min_length')

    @property
    def policy_text(self):
        """Method to return message."""
        return self.text.format(min_length=self.min_length)


class PasswordContains(PasswordStrengthPolicy):
    """Base class which validates if passwords contain at least a certain.

    number of characters from a certain set.
    """

    chars = None
    min_count = 1
    text = None
    plural_text = None

    def validate(self, value, user=None):
        """Method to do the validation."""
        pw_set = set(value)
        if len(pw_set.intersection(self.chars)) < self.min_count:
            raise ValidationError(self.text, 'password_complexity')

    @property
    def policy_text(self):
        """Some policy text."""
        if self.min_count > 1:
            return self.plural_text.format(min_count=self.min_count)
        else:
            return self.text.format(min_count=self.min_count)

    @property
    def policy_caption(self):
        """Some caption message."""
        return self.chars


class PasswordContainsUpperCase(PasswordContains):
    """Class to handle upper case."""

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = _('Passwords must have at least one uppercase character.')
    plural_text = _('Passwords must have at least {min_count} '
                    'uppercase characters.')


class PasswordContainsLowerCase(PasswordContains):
    """Class to handle lower case."""

    chars = 'abcdefghijklmnopqrstuvwxyz'
    text = _('Passwords must have at least one lowecase character.')
    plural_text = _('Passwords must have at least {min_count} '
                    'lowercase characters.')


class PasswordContainsNumbers(PasswordContains):
    """Class to handle Numbers."""

    chars = '0123456789'
    text = _('Passwords must have at least one number.')
    plural_text = _('Passwords must have at least {min_count} '
                    'numbers.')


class PasswordContainsSymbols(PasswordContains):
    """Class to handle Symbols."""

    chars = '!@#$%^&*()_+-={}[]:;"\'|\\,.<>?/~` '
    text = _('Passwords must have at least one special character.')
    plural_text = _('Passwords must have at least {min_count} special '
                    'characters (punctuation).')


class PasswordContainsAlphabetics(PasswordContains):
    """Class to handle alphabetics."""

    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = _('Passwords must have at least one alphabetic character.')
    plural_text = _('Passwords must have at least {min_count} '
                    'alphabetic characters.')


class PasswordUserAttrs(PasswordStrengthPolicy):
    """Validate if password doesn't contain values from a list of user.

    attributes. Every attribute will be normalized into ascii and split
    on non alphanumerics.

    Use this in the clean method of password forms

    `value`: password
    `user`: user object with attributes

    Example, which would raise a ValidationError:

        user.first_name = 'John'
        password_user_attrs('johns_password', user)
    """

    user_attrs = ('email', 'first_name', 'last_name', 'username')
    text = _('Passwords are not allowed to contain (pieces of) your name '
             'or email.')

    _non_alphanum = re.compile(r'[^a-z0-9]')

    def validate(self, value, user=None):
        """Method to validate alphabetics."""
        if user is None:
            return

        simple_pass = _normalize_unicode(value)
        for attr in self.user_attrs:
            v = getattr(user, attr, None)
            if not attr or len(attr) < 4:
                continue

            v = _normalize_unicode(v)

            for piece in self._non_alphanum.split(v):
                if len(piece) < 4:
                    continue

                if piece in simple_pass:
                    raise ValidationError(self.text, 'password_user_attrs')

    @property
    def policy_text(self):
        """Method to return policy text."""
        return self.text


class PasswordDisallowedTerms(PasswordStrengthPolicy):
    """Disallow a (short) list of terms in passwords.

    Ideal for too obvious terms like the name of the site or company
    """

    terms = None
    text = _('Passwords are not allowed to contain the following term(s): '
             '{terms}.')
    show_policy = False

    def __init__(self, **kwargs):
        """Constructor for terms."""
        terms = kwargs.pop('terms')
        self.terms = [_normalize_unicode(term) for term in terms]

        super(PasswordDisallowedTerms, self).__init__(**kwargs)

    def validate(self, value, user=None):
        """Method to validate terms."""
        simple_pass = _normalize_unicode(value)
        found = []
        for term in self.terms:
            if term in simple_pass:
                found.append(term)

        if found:
            msg = self.text.format(terms=u', '.join(found))
            raise ValidationError(msg, 'password_disallowed_terms')

    @property
    def policy_text(self):
        """For users not to disobet terms."""
        return self.text.format(terms=u', '.join(self.terms))


class PasswordLimitReuse(PasswordStrengthPolicy):
    """Limits reuse of previous passwords.

    Use this to prevent users from reusing one of their previous passwords.
    """

    max_pw_history = 3
    text = _('New password must be different than your last password.')
    plural_text = _('New password must not be one of your last '
                    '{max_pw_history} passwords.')

    def validate(self, value, user=None):
        """Method to validate the limite re-use of passwords."""
        if user is None:
            return

        last_pw_changes = PasswordChange.objects.filter(
            user=user, successful=True).order_by('-id')[:self.max_pw_history]

        for pw_change in last_pw_changes:
            if check_password(value, pw_change.password):
                raise ValidationError(self.policy_text, 'password_limit_reuse')

    @property
    def policy_text(self):
        """For users not to re-use passwords."""
        if self.max_pw_history > 1:
            return self.plural_text.format(max_pw_history=self.max_pw_history)
        else:
            return self.text.format(max_pw_history=self.max_pw_history)
