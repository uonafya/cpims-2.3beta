"""Test API for users."""
from rest_framework import viewsets
from .serializers import UserSerializer, OrgUnitSerializer
from cpovc_auth.models import AppUser
from cpovc_registry.models import RegOrgUnit


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = AppUser.objects.all().order_by('-last_login')
    serializer_class = UserSerializer


class OrgUnitsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows Organisation Units to be viewed or edited."""

    queryset = RegOrgUnit.objects.filter(
        is_void=False).order_by('org_unit_name')
    serializer_class = OrgUnitSerializer
