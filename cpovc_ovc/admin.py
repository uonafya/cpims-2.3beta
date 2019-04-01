"""Admin backend for editing this aggregate data."""
import csv
import time
from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from .models import (
    OVCAggregate, OVCFacility, OVCSchool, OVCCluster,
    OVCClusterCBO, OVCRegistration)


def dump_to_csv(modeladmin, request, qs):
    """
    These takes in a Django queryset and spits out a CSV file.

    Generic method for any queryset
    """
    model = qs.model
    file_id = 'CPIMS_%s_%d' % (model.__name__, int(time.time()))
    file_name = 'attachment; filename=%s.csv' % (file_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = file_name
    writer = csv.writer(response, csv.excel)

    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)

    for obj in qs:
        row = []
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row.append(val)
        writer.writerow(row)
    return response
dump_to_csv.short_description = u"Dump to CSV"


class OVCRegistrationAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['person',]
    list_display = ['id', 'person', 'child_cbo', 'child_chv',
                    'caretaker', 'registration_date', 'hiv_status',
                    'is_active', 'is_void']
    readonly_fields = ['id', 'person', 'caretaker', 'child_chv']
    list_filter = ['is_active', 'is_void', 'hiv_status']


admin.site.register(OVCRegistration, OVCRegistrationAdmin)

class OVCAggregateAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['indicator_name', 'gender']
    list_display = ['id', 'indicator_name', 'indicator_count', 'age',
                    'reporting_period', 'cbo', 'subcounty', 'county']
    # readonly_fields = ['id']
    list_filter = ['indicator_name', 'project_year', 'reporting_period',
                   'gender', 'subcounty', 'county', 'cbo']


admin.site.register(OVCAggregate, OVCAggregateAdmin)


class OVCFacilityAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['facility_code', 'facility_name']
    list_display = ['id', 'facility_code', 'facility_name',
                    'sub_county']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    actions = [dump_to_csv]


admin.site.register(OVCFacility, OVCFacilityAdmin)


class OVCSchoolAdmin(ImportExportModelAdmin):
    """Aggregate data admin."""

    search_fields = ['school_name']
    list_display = ['id', 'school_level', 'school_name',
                    'sub_county']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    actions = [dump_to_csv]


admin.site.register(OVCSchool, OVCSchoolAdmin)


class CBOsInline(admin.StackedInline):
    model = OVCClusterCBO
    # exclude = ('password', )


class OVCClusterAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['cluster_name']
    list_display = ['id', 'cluster_name', 'created_by']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    inlines = (CBOsInline, )
    actions = [dump_to_csv]


admin.site.register(OVCCluster, OVCClusterAdmin)


class OVCClusterCBOAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['cluster', 'cbo']
    list_display = ['id', 'cluster', 'cbo', 'added_at']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(OVCClusterCBO, OVCClusterCBOAdmin)
