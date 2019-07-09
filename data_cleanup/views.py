import os
import pydoc
from subprocess import call

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .clean_data import get_model_fields
from .models import DataQuality


class DataQualityView(TemplateView):
    template_name = 'data_cleanup/filter.html'
    
    def get_context_data(self, **kwargs):
        context = super(DataQualityView, self).get_context_data(**kwargs)
        context['data'] = self.get_queryset()
        return context

    def get_queryset(self, *args, **kwargs):
        return []
    
    def get(self, *args, **kwargs):
        if self.request.GET.dict().get('export', False):
            return self.export_data(*args, **kwargs)
        else:
            return super(DataQualityView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        context = {}
        queryset =  DataQuality.objects.all()
        age = self.request.POST.get('age')
        age_operator = self.request.POST.get('operator')
        school_level = self.request.POST.get('school_level')
        hiv_status = self.request.POST.get('hiv_status')
        art_status = self.request.POST.get('art_status')
        
        if age:
            if  age_operator == '-' and age_operator != '0':
                ages =  age.split('-')
                if len(ages) != 2:
                    context['error'] = 'Please supply the min and max age e.g 19-20'
                    return TemplateResponse(self.request, self.template_name, context) 
                else:
                    try:
                        min_age = int(ages[0])
                        max_age = int(ages[1])
                        queryset = queryset.filter(age__gte=min_age, age__lte=max_age)
                    except ValueError:
                        context['error'] = 'Please use numbers for age'
                        return TemplateResponse(self.request, self.template_name, context)
                    
            elif age_operator == '=':
                queryset =  queryset.filter(age=age)
            elif age_operator == '>':
                queryset =  queryset.filter(age__gt=age) 
            elif  age_operator == '<':
                queryset = queryset.filter(age__lt=age)
        

        if school_level and school_level != '0':
            queryset = queryset.filter(school_level=school_level)
        
        if hiv_status and hiv_status != '0':
            queryset = queryset.filter(hiv_status=hiv_status)

        if art_status and art_status != '0':
            queryset = queryset.filter(art_status=art_status)

        context['data']= queryset
        return TemplateResponse(self.request, self.template_name, context)
    
    def export_data(self, *args, **kwargs):
        call('bin/export_data.sh {} {} {} {} '.format(
            '41.89.93.206','postgres', 'cpims', '/tmp/file.csv'), 
            shell=True
        )
        file_name = '/tmp/file.csv'
        path_to_file = '/tmp/file.csv'
        with open(path_to_file, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path_to_file)
            return response
        return HttpResponse("Bad Request")