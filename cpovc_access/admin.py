"""For admin view."""
import logging
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import password_change
from django.contrib import messages

from cpovc_access.forms import StrictPasswordChangeForm
from cpovc_access.models import AccessLog, AccessAttempt
from cpovc_access.models import PasswordChange, UserChange

logger = logging.getLogger(__name__)


def unlock_user(modeladmin, request, queryset):
    """
    These takes in a Django queryset and spits out a CSV file.

    Generic method for any queryset
    """
    # model = qs.model
    queryset.update(failures_since_start=0)
    message = ('User(s) failed login counts reset to 0. '
               'User(s) can now log in.')
    messages.info(request, message)

unlock_user.short_description = u"Unlock selected user(s)"


class AccessAttemptAdmin(admin.ModelAdmin):
    """Class for handling attempts."""

    list_display = (
        'attempt_time',
        'ip_address',
        'user_agent',
        'username',
        'path_info',
        'failures_since_start',
    )

    list_filter = [
        'attempt_time',
        'ip_address',
        'username',
        'path_info',
    ]

    search_fields = [
        'ip_address',
        'username',
        'user_agent',
        'path_info',
    ]

    date_hierarchy = 'attempt_time'

    fieldsets = (
        (None, {
            'fields': ('path_info', 'failures_since_start')
        }),
        ('Form Data', {
            'fields': ('get_data', 'post_data')
        }),
        ('Meta Data', {
            'fields': ('user_agent', 'ip_address', 'http_accept')
        })
    )

    actions = [unlock_user]

admin.site.register(AccessAttempt, AccessAttemptAdmin)


class AccessLogAdmin(admin.ModelAdmin):
    """Class for handling access logs."""

    list_display = (
        'attempt_time',
        'logout_time',
        'ip_address',
        'username',
        'user_agent',
        'path_info',
    )

    list_filter = [
        'attempt_time',
        'logout_time',
        'ip_address',
        'username',
        'path_info',
    ]

    search_fields = [
        'ip_address',
        'user_agent',
        'username',
        'path_info',
    ]

    date_hierarchy = 'attempt_time'

    fieldsets = (
        (None, {
            'fields': ('path_info',)
        }),
        ('Meta Data', {
            'fields': ('user_agent', 'ip_address', 'http_accept')
        })
    )

admin.site.register(AccessLog, AccessLogAdmin)


def admin_login(request, extra_context=None):
    """Redirect to default login view which enforces auth policy."""
    next_page = request.get_full_path()
    next_url = next_page.split('=')[1] if '=' in next_page else next_page
    q = REDIRECT_FIELD_NAME + '=' + next_url
    return HttpResponseRedirect(reverse('login') + '?' + q)


admin.site.login = admin_login


def admin_logout(request, extra_context=None):
    """Redirect to default login page and not /admin area."""
    return HttpResponseRedirect(reverse('login'))


admin.site.logout = admin_logout


class PasswordChangeAdmin(admin.ModelAdmin):
    """Class to handle password change."""

    readonly_fields = ('user', 'timestamp', 'successful', 'is_temporary')
    fields = ('user', 'timestamp', 'successful', 'is_temporary')
    list_display = ('user', 'successful', 'is_temporary', 'timestamp')
    list_filter = ('successful', 'is_temporary')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        """Method to handle add permissions."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Method to handle delete permission."""
        return False

    def save_model(self, request, obj, form, change):
        """Do not actually save anything to prevent changes."""
        logger.info('Prevented change in PasswordChange item by user %s',
                    request.user)

    def get_actions(self, request):
        """Disable deletion of user changes action."""
        actions = super(PasswordChangeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(PasswordChange, PasswordChangeAdmin)


class UserChangeAdmin(admin.ModelAdmin):
    """Class to handle user changes."""

    readonly_fields = ('user', 'timestamp', 'by_user')
    fields = ('user', 'timestamp', 'by_user')
    list_display = ('user', 'by_user', 'timestamp')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        """Method to handle add permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Method to handle delete permission."""
        return False

    def save_model(self, request, obj, form, change):
        """Do not actually save anything to prevent changes."""
        logger.info('Prevented change in UserChange item by user %s',
                    request.user)

    def get_actions(self, request):
        """Disable deletion of user changes action."""
        actions = super(UserChangeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(UserChange, UserChangeAdmin)


def admin_password_change(request):
    """Handle the "change password" task - both display and validation."""
    to_url = reverse('admin:password_change_done', current_app=admin.site.name)
    defaults = {
        'current_app': admin.site.name,
        'post_change_redirect': to_url,
        'password_change_form': StrictPasswordChangeForm
    }
    if admin.site.password_change_template is not None:
        defaults['template_name'] = admin.site.password_change_template
    return password_change(request, **defaults)

admin.site.password_change = admin_password_change
