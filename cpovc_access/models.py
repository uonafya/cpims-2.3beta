"""Access handler models."""
from django.db import models
from django.utils import six
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string

from cpovc_access.settings import TEMP_PASSWORD_LENGTH, TEMP_PASSWORD_CHARS


class CommonAccess(models.Model):
    """Common access class."""

    user_agent = models.CharField(
        max_length=255,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name='IP Address',
        null=True,
    )

    username = models.CharField(
        max_length=255,
        null=True,
    )

    # Once a user logs in from an ip, that combination is trusted and not
    # locked out in case of a distributed attack
    trusted = models.BooleanField(
        default=False,
    )

    http_accept = models.CharField(
        verbose_name='HTTP Accept',
        max_length=1025,
    )

    path_info = models.CharField(
        verbose_name='Path',
        max_length=255,
    )

    attempt_time = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Override some values."""

        abstract = True
        ordering = ['-attempt_time']


class AccessAttempt(CommonAccess):
    """Access attempt class."""

    get_data = models.TextField(
        verbose_name='GET Data',
    )

    post_data = models.TextField(
        verbose_name='POST Data',
    )

    failures_since_start = models.PositiveIntegerField(
        verbose_name='Failed Logins',
    )

    @property
    def failures(self):
        """To return failures values."""
        return self.failures_since_start

    def __unicode__(self):
        """For the admin."""
        return six.u('Attempted Access: %s') % self.attempt_time

    class Meta:
        """Override some values."""

        db_table = 'auth_login_attempt'


class AccessLog(CommonAccess):
    """Access log class."""

    logout_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        """For admin."""
        return six.u('Access Log for %s @ %s') % (self.username,
                                                  self.attempt_time)

    class Meta:
        """Override some values."""

        db_table = 'auth_login_accesslog'


class AccessRequest(models.Model):
    """Model for guests access request."""

    names = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    ip_address = models.GenericIPAddressField(protocol='both')
    timestamp_requested = models.DateTimeField(auto_now=True)

    class Meta:
        """Override table details."""

        db_table = 'auth_login_request'


class PasswordChangeAdmin(models.Manager):
    """Password change admin handler."""

    def set_temporary_password(self, user):
        """Will return a random password and set as temporary password."""
        password = get_random_string(TEMP_PASSWORD_LENGTH, TEMP_PASSWORD_CHARS)

        pw_change = PasswordChange(user=user, is_temporary=True,
                                   successful=True)
        pw_change.set_password(password)
        pw_change.save()

        user.set_password(password)
        user.save()

        return password


class PasswordChange(models.Model):
    """Password change model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             blank=True, null=True, on_delete=models.SET_NULL)
    user_repr = models.CharField(_('user'), max_length=200)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    successful = models.BooleanField(_('successful'), default=False)
    is_temporary = models.BooleanField(_('is temporary'), default=False)
    password = models.CharField(_('password'), max_length=128, default='',
                                editable=False)

    objects = PasswordChangeAdmin()

    class Meta:
        """Override some values."""

        db_table = 'auth_password_history'
        verbose_name = _('password change')
        verbose_name_plural = _('password changes')
        ordering = ('-id',)

    def set_password(self, raw_password):
        """Method to set the password."""
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        """Method to do the actual save of data."""
        if self.user_id is not None and not self.user_repr:
            self.user_repr = self.user.get_username()[:200] or 'NO USERNAME'
            if kwargs.get('update_fields'):
                kwargs['update_fields'].append('user_repr')
        super(PasswordChange, self).save(*args, **kwargs)

    def __unicode__(self):
        """Override the return results."""
        return u'{0} at {1}'.format(self.user, self.timestamp)


class UserChange(models.Model):
    """Model to track user changes."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             blank=True, null=True, on_delete=models.SET_NULL)
    user_repr = models.CharField(_('user'), max_length=200)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    by_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('by user'),
                                related_name='changed_users',
                                blank=True, null=True,
                                on_delete=models.SET_NULL)
    by_user_repr = models.CharField(_('by user'), max_length=200)

    class Meta:
        """Override some values."""

        db_table = 'auth_user_history'
        verbose_name = _('user change')
        verbose_name_plural = _('user changes')
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        """Override save method."""
        if self.user_id is not None and not self.user_repr:
            self.user_repr = self.user.get_username()[:200] or 'NO USERNAME'
            if kwargs.get('update_fields'):
                kwargs['update_fields'].append('user_repr')

        if self.by_user_id is not None and not self.by_user_repr:
            self.by_user_repr = (self.by_user.get_username()[:200] or
                                 'NO USERNAME')
            if kwargs.get('update_fields'):
                kwargs['update_fields'].append('by_user_repr')

        super(UserChange, self).save(*args, **kwargs)

    def __unicode__(self):
        """Some return message for the admin."""
        return u'{0} at {1} by {1}'.format(self.user, self.timestamp,
                                           self.by_user)


class LoginAttemptManager(models.Manager):
    """Manager to handle Logins."""

    def unlock(self, usernames=[], addresses=[]):
        """To Unlock given usernames and IP addresses.

        Returns the number of attempts that have been unlocked.
        """
        if not usernames and not addresses:
            return 0

        selection = models.Q()

        if usernames:
            selection |= models.Q(username__in=set(usernames))

        if addresses:
            selection |= models.Q(source_address__in=set(addresses))

        return self.get_queryset().filter(
            selection, lockout=True).update(lockout=False)

    def unlock_queryset(self, queryset):
        """To unlock all usernames and IP addresses found in ``queryset``.

        Returns the number of attempts that have been unlocked.
        """
        selected_attempts = queryset.filter(
            lockout=True).order_by().values_list('username', 'source_address')

        if not selected_attempts:
            return 0

        usernames, addresses = zip(*selected_attempts)

        return self.unlock(usernames=usernames, addresses=addresses)


class LoginAttempt(models.Model):
    """Track logins."""

    username = models.CharField(_('username'), max_length=100, db_index=True)
    source_address = models.GenericIPAddressField(
        _('source address'), protocol='both', db_index=True)
    hostname = models.CharField(_('hostname'), max_length=100)
    successful = models.BooleanField(_('successful'), default=False)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True,
                                     db_index=True)
    # User fields are only filled at successful login attempts:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             blank=True, null=True, on_delete=models.SET_NULL)
    user_repr = models.CharField(_('user'), blank=True, max_length=200)
    # This is enabled for all failed login attempts. It is reset for every
    # successful login and can be reset by 'user admins'.
    lockout = models.BooleanField(_('lockout'), default=True,
                                  help_text=_('Counts towards lockout count'))

    objects = LoginAttemptManager()

    class Meta:
        """Overrride some values."""

        db_table = 'auth_login_policy'
        verbose_name = _('login attempt')
        verbose_name_plural = _('login attempts')
        ordering = ('-id',)
        permissions = (
            ('unlock', _('Unlock by username or IP address')),
        )

    def save(self, *args, **kwargs):
        """To do the actual save."""
        if self.user_id is not None and not self.user_repr:
            self.user_repr = self.user.get_username()[:200] or 'NO USERNAME'
            if kwargs.get('update_fields'):
                kwargs['update_fields'].append('user_repr')
        super(LoginAttempt, self).save(*args, **kwargs)

    def __unicode__(self):
        """Some return text."""
        return u'{0} at {1} from {2}'.format(self.username,
                                             self.timestamp,
                                             self.source_address)
