from django.views.generic import TemplateView
from django.template.response import TemplateResponse
import pydoc

from .clean_data import get_model_fields
from .models import DataQuality


class DataQualityView(TemplateView):
    template_name = 'data_cleanup/filter.html'
    
    def get_context_data(self, **kwargs):
        context = super(DataQualityView, self).get_context_data(**kwargs)
        context['data'] = self.get_queryset()
        return context

    def get_queryset(self, *args, **kwargs):
        return DataQuality.objects.all()[0:100]
    
    def post(self, *args, **kwargs):
        context = {}
        queryset =  DataQuality.objects.all()[0:100]
        age = self.request.POST.get('age')
        age_operator = self.request.POST.get('operator')
        school_level = self.request.POST.get('school_level')

        if age_operator == '=':
            queryset =  queryset.filter(age=age)
        elif age_operator == '>':
            queryset =  queryset.filter(age__gt=age) 
        elif  age_operator == '<':
            queryset = queryset.filter(age__lt=age)

        if school_level:
            queryset = queryset.filter(school_level=school_level)

        context['data']= queryset
        return TemplateResponse(self.request, self.template_name, context)