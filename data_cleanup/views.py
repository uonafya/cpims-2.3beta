from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
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

        if age_operator == '=':
            queryset =  queryset.filter(age=age)
        elif age_operator == '>':
            queryset =  queryset.filter(age__gt=age) 
        elif  age_operator == '<':
            queryset = queryset.filter(age__lt=age)

        if school_level:
            queryset = queryset.filter(school_level=school_level)
        # queryset = Paginator(queryset, 30)
        context['data']= queryset
        return TemplateResponse(self.request, self.template_name, context)
    
    def export_data(self, *args, **kwargs):
        from subprocess import call
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import os
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