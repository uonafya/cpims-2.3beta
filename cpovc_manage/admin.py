from django.contrib import admin
from .models import NOTTTravel, NOTTChild, NOTTChaperon


class NOTTChaperonInline(admin.TabularInline):
    model = NOTTChaperon
    fields = ('other_person', 'sex', 'passport')
    readonly_fields = ['other_person', 'sex', 'passport']
    extra = 0
    can_delete = False
    verbose_name = 'Name of Chaperon'
    verbose_name_plural = 'Names of Chaperons'

    def sex(self, obj):
        sex_id = obj.other_person.person_sex
        sex = 'Male' if sex_id == 'SMAL' else 'Female'
        return sex

    def passport(self, obj):
        return obj.other_person.person_identifier
    # list_editable = ['other_person']
    # exclude = ('password', )


class NOTTChildInline(admin.TabularInline):
    model = NOTTChild
    fields = ('person', 'sex', 'cleared', 'returned', 'passport')
    readonly_fields = ['person', 'sex', 'cleared',
                       'returned', 'passport']
    extra = 0
    can_delete = False
    verbose_name = 'Name of Child'
    verbose_name_plural = 'Names of Children'

    def sex(self, obj):
        sex_id = obj.person.sex_id
        sex = 'Male' if sex_id == 'SMAL' else 'Female'
        return sex


class TravelAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['institution_name', 'reason', 'id']
    list_display = ['id', 'institution_name', 'travel_date', 'return_date',
                    'sponsor', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'sponsor', 'timestamp_created', 'travel_date']

    inlines = (NOTTChaperonInline, NOTTChildInline, )


admin.site.register(NOTTTravel, TravelAdmin)
