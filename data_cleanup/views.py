import os
import pydoc
from subprocess import call

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView


from cpovc_registry.models import RegPerson, RegPersonsOrgUnits
from cpovc_auth.functions import get_allowed_units_county
from .models import DataQuality


class DataQualityView(TemplateView):
    template_name = 'data_cleanup/filter.html'
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        context = super(
            DataQualityView, self).get_context_data(**kwargs)
        context['data'] = self.get_queryset()
        return context

    def get_final_query_set(self, queryset):
        allowed_org_units = [
            obj.id for obj in RegPersonsOrgUnits.objects.filter(
                person=self.request.user.reg_person)
        ]
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(org_unique_id__in=allowed_org_units)

    def get_queryset(self, *args, **kwargs):
        return []

    def get(self, *args, **kwargs):
        if self.request.GET.dict().get('export', False):
            return self.export_data(*args, **kwargs)
        else:
            return super(DataQualityView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        objs = get_allowed_units_county(self.request.user.id)
        context = {}
        queryset =  DataQuality.objects.all()
        age = self.request.POST.get('age')
        age_operator = self.request.POST.get('operator')
        school_level = self.request.POST.get('school_level')
        hiv_status = self.request.POST.get('hiv_status')
        art_status = self.request.POST.get('art_status')
        gender = self.request.POST.get('gender')
        is_disabled = self.request.POST.get('is_disabled')
        is_ovc = self.request.POST.get('is_ovc')
        has_bcert = self.request.POST.get('has_bcert')

        # Maintain selected options in the views
        view_filter_values = {
            'age': age
        }

        filters = {}
        if age:
            if  age_operator == '-' and age_operator != '0':
                ages =  age.split('-')
                if len(ages) != 2:
                    error = 'Please supply the min and max age e.g 19-20'
                    context['error'] = error
                    return TemplateResponse(
                    self.request, self.template_name, context)
                else:
                    try:
                        min_age = int(ages[0])
                        max_age = int(ages[1])

                        view_filter_values['between'] = True

                        queryset = queryset.filter(
                            age__gte=min_age, age__lte=max_age)
                    except ValueError:
                        context['error'] = 'Please use numbers for age'
                        return TemplateResponse(
                            self.request, self.template_name, context)

            elif age_operator == '=':
                queryset =  queryset.filter(age=age)
                view_filter_values['equals'] = True
            elif age_operator == '>':
                queryset =  queryset.filter(age__gt=age)
                view_filter_values['greater_than'] = True
            elif  age_operator == '<':
                view_filter_values['less_than'] = True
                queryset = queryset.filter(age__lt=age)

        if school_level and school_level != '0':
            filters['school_level'] = school_level
            if school_level == 'SLSE':
                view_filter_values['slse'] = True
            if school_level == 'SLPR':
                view_filter_values['slpr'] = True
            if school_level == 'SLNS':
                view_filter_values['slns'] = True

        if hiv_status and hiv_status != '0':
            filters['hiv_status'] = hiv_status
            if hiv_status == 'HSTR':
                view_filter_values['hstr'] = True
            if hiv_status == 'HSKN':
                view_filter_values['hskn'] = True
            if hiv_status == 'HSTP':
                view_filter_values['hstp'] = True
            if hiv_status == 'XXXX':
                view_filter_values['xxxx'] = True
            if hiv_status == 'HSTN':
                view_filter_values['hstn'] = True
            if hiv_status == 'HSRT':
                view_filter_values['hsrt'] = True
            if hiv_status == 'HSTR':
                view_filter_values['hstr'] = True

        if art_status and art_status != '0':
            filters['art_status'] = art_status
            if art_status == 'ARV':
                view_filter_values['arv'] = True
            if art_status == 'ART':
                view_filter_values['art'] = True
            if art_status == 'ARAR':
                view_filter_values['arar'] = True

        if is_disabled and is_disabled == 'True':
            filters['is_disabled'] = True
            view_filter_values['is_disabled_yes'] = True

        if is_disabled and is_disabled == 'False':
            filters['is_disabled'] = False
            view_filter_values['is_disabled_no'] = True

        if gender and gender != '0':
            filters['sex_id'] = gender
            if gender == 'SMAL':
                view_filter_values['smal'] = True
            if gender == 'SFEM':
                view_filter_values['sfem'] = True
        if is_ovc and is_ovc != '0':
            filters['designation'] = is_ovc
            if is_ovc == 'CCGV':
                view_filter_values['ccgv'] = True
            if is_ovc == 'COSI':
                view_filter_values['cosi'] = True
            if is_ovc == 'COVC':
                view_filter_values['covc'] = True
            if is_ovc == 'CGOC':
                view_filter_values['cgoc'] = True

        if has_bcert and has_bcert == 'True':
            filters['has_bcert'] = True
            view_filter_values['has_bcert_yes'] = True

        if has_bcert and has_bcert == 'False':
            filters['has_bcert'] = False
            view_filter_values['has_bcert_no'] = True

        queryset = queryset.filter(**filters)
        context['data']= queryset
        context['view_filter_values'] = view_filter_values
        return TemplateResponse(self.request, self.template_name, context)

    def generate_where_clause(self):
        query_dict = self.request.GET.dict()
        school_level = query_dict.get('school_level')
        age = query_dict.get('age')
        operator = query_dict.get('operator')
        art_status = query_dict.get('art_status')
        hiv_status = query_dict.get('hiv_status')
        sql = "WHERE 1=1 AND "
        if school_level != '0':
            sql += "school_level='{}' AND ".format(school_level)
        if age:
            sql += "age='{}' AND ".format(age)
        if art_status != '0':
            sql += "art_status='{}' AND ".format(art_status)
        if hiv_status != '0':
            sql += "hiv_status='{}' AND ".format(hiv_status)
        sql += '1=1'
        return sql
