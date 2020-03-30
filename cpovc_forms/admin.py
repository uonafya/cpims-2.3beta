from django.contrib import admin
from .models import OVCCareQuestions, OVCCareForms


# Register your models here.
class OVCCareFormsInline(admin.TabularInline):
    model = OVCCareQuestions


class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_void', 'timestamp_created', 'timestamp_updated')
    search_fields = ('name',)
    inlines = [
        OVCCareFormsInline
    ]


admin.site.register(OVCCareForms, FormAdmin)
