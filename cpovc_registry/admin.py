"""Admin backend for editing some admin details."""
import csv
import time
from django.contrib import admin
from django.http import HttpResponse
from .models import (RegPerson, RegOrgUnit, RegOrgUnitsAuditTrail,
                     RegPersonsAuditTrail, RegPersonsTypes)


from cpovc_auth.models import AppUser

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


class PersonInline(admin.StackedInline):
    model = AppUser
    exclude = ('password', )


class RegPersonAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['first_name', 'surname', 'other_names']
    list_display = ['id', 'first_name', 'surname', 'date_of_birth',
                    'age', 'sex_id', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'sex_id', 'created_at']

    inlines = (PersonInline, )


admin.site.register(RegPerson, RegPersonAdmin)


class RegPersonTypesAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person__surname', 'person__first_name']
    list_display = ['id', 'person', 'person_type_id',
                    'date_created', 'is_void', ]

    def date_created(self, obj):
        return obj.person.created_at
    date_created.admin_order_field = 'date'
    date_created.short_description = 'Date Created'
    readonly_fields = ['person']
    list_filter = ['is_void', 'person_type_id', 'person__created_at']


admin.site.register(RegPersonsTypes, RegPersonTypesAdmin)


class RegOrgUnitAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_name', 'org_unit_id_vis']
    list_display = ['id', 'org_unit_id_vis', 'org_unit_name',
                    'parent_org_unit_id', 'parent_unit', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'org_unit_type_id', 'created_at',
                   'parent_org_unit_id']
    actions = [dump_to_csv]


admin.site.register(RegOrgUnit, RegOrgUnitAdmin)


class OrgUnitAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']


admin.site.register(RegOrgUnitsAuditTrail, OrgUnitAuditAdmin)


class PersonsAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']


admin.site.register(RegPersonsAuditTrail, PersonsAuditAdmin)
