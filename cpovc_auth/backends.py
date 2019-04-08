from cpovc_auth.models import AppUser
from django.contrib.auth.models import check_password
from django.contrib.auth.backends import ModelBackend
from django.conf import settings


class CPOVCAuthenticationBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on workforce_id / national_id. """
        try:
            user = AppUser.objects.get(username__iexact=username.lower())
            if settings.ALLOW_NATIONAL_ID_LOGIN:
                if not user:
                    user = AppUser.objects.get(national_id=username)
            if user and check_password(password, user.password):
                return user
        except AppUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Get a AppUser object from the user_id. """
        try:
            return AppUser.objects.get(pk=user_id)
        except AppUser.DoesNotExist:
            return None
