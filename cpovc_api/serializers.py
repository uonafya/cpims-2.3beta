"""Serializers for the test API."""
from cpovc_auth.models import AppUser
from cpovc_registry.models import RegOrgUnit
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """Overrride parameters."""

        model = AppUser
        fields = ('first_name', 'surname', 'id')


class OrgUnitSerializer(serializers.HyperlinkedModelSerializer):
    """Organisation Unit serializer."""

    class Meta:
        """Overrride parameters."""

        model = RegOrgUnit
        fields = ('org_unit_id_vis', 'org_unit_name', 'id')
        read_only_fields = ('org_unit_id_vis', 'org_unit_name')
