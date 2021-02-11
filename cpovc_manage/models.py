from django.db import models
from django.utils import timezone
from cpovc_forms.models import OvcCasePersons
from cpovc_registry.models import RegPerson, RegPersonsExternalIds


class NOTTTravel(models.Model):
    """Master Facility list model."""

    institution_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=150)
    travel_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    no_applied = models.IntegerField(default=0)
    no_cleared = models.IntegerField(default=0)
    no_returned = models.IntegerField(default=0, null=True, blank=True)
    contacts = models.CharField(max_length=150, null=True, blank=True)
    reason = models.CharField(max_length=150)
    sponsor = models.CharField(max_length=100)
    comments = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'nott_travel'
        verbose_name = 'Non Objection to Travel - Travel'
        verbose_name_plural = 'Non Objection to Travel - Travels'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.institution_name)


class NOTTChaperon(models.Model):
    """Master Facility list model."""

    travel = models.ForeignKey(NOTTTravel, on_delete=models.CASCADE)
    other_person = models.ForeignKey(OvcCasePersons, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'nott_chaperon'
        verbose_name = 'Non Objection to Travel - Chaperon'
        verbose_name_plural = 'Non Objection to Travel - Chaperons'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.other_person)


class NOTTChild(models.Model):
    """Master Facility list model."""

    travel = models.ForeignKey(NOTTTravel, on_delete=models.CASCADE)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)

    def _passport(self):
        _ppt = RegPersonsExternalIds.objects.get(
            person_id=self.person_id, is_void=False,
            identifier_type_id='IPPN')
        return _ppt

    passport = property(_passport)

    class Meta:
        """Override some params."""

        db_table = 'nott_child'
        verbose_name = 'Non Objection to Travel - Child'
        verbose_name_plural = 'Non Objection to Travel - Children'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.person)
