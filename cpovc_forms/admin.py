from django.contrib import admin
from .models import OVCCareQuestions


# Register your models here.
class OVCCareQuestionsAdmin(admin.ModelAdmin):
    list_display = ('code', 'question', 'question_type', 'domain', 'question_text', 'is_void')
    search_fields = ['code', 'question', 'domain', 'question_type']


admin.site.register(OVCCareQuestions, OVCCareQuestionsAdmin)
