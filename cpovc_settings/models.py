import uuid
from django.db import models
from cpovc_forms.models import OVCCaseRecord
from cpovc_registry.models import RegPerson, RegOrgUnit
from django.utils import timezone
from cpovc_auth.models import AppUser


class CaseDuplicates(models.Model):
    """Model for managing duplicate cases."""

    duplicate_id = models.UUIDField(default=uuid.uuid4, editable=False)
    case_category_id = models.CharField(max_length=4)
    person = models.ForeignKey(RegPerson)
    organization_unit = models.ForeignKey(RegOrgUnit)
    case = models.ForeignKey(OVCCaseRecord)
    created_by = models.ForeignKey(AppUser, null=True, related_name='creator')
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(AppUser, null=True, related_name='updator')
    updated_at = models.DateTimeField(null=True)
    action_id = models.IntegerField(default=1)
    interventions = models.IntegerField(default=0)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'case_duplicates'
        verbose_name = 'Duplicated case'
        verbose_name_plural = 'Duplicated Cases'
