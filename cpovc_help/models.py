import os
from django.db import models
from cpovc_registry.models import RegPerson


class OVCDownloads(models.Model):
    doc_type = models.IntegerField()
    name = models.CharField(max_length=255)
    version = models.DecimalField(max_digits=5, decimal_places=2)
    doc_date = models.DateField()
    doc_details = models.TextField()
    downloads = models.BigIntegerField(default=0)
    doc_tags = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents')
    person = models.ForeignKey(RegPerson, null=True)
    is_public = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)

    def _filename(self):
        return os.path.basename(self.document.name)

    def _filesize(self):
        return self.document.size

    filename = property(_filename)
    filesize = property(_filesize)

    class Meta:
        """Override table details."""

        db_table = 'ovc_downloads'
        verbose_name = 'DCS / OVC Document'
        verbose_name_plural = 'DCS / OVC Documents'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.name


class OVCFAQ(models.Model):
    faq_order = models.IntegerField(default=1)
    faq_title = models.CharField(max_length=255)
    faq_details = models.TextField()
    faq_timestamp = models.DateTimeField()
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_faq'
        verbose_name = 'FAQ Detail'
        verbose_name_plural = 'FAQ Details'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.faq_title
