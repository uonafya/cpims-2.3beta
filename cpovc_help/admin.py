from django.contrib import admin
from .models import OVCDownloads, OVCFAQ


class OVCDownloadsAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['name', 'doc_tags']
    list_display = ['name', 'doc_date', 'version', 'downloads', 'is_void']
    readonly_fields = ['person']
    list_filter = ['is_void', 'doc_date']


admin.site.register(OVCDownloads, OVCDownloadsAdmin)


class OVCFAQAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['faq_title']
    list_display = ['faq_title', 'faq_order', 'faq_timestamp', 'is_void']
    list_filter = ['is_void', 'faq_timestamp']


admin.site.register(OVCFAQ, OVCFAQAdmin)
