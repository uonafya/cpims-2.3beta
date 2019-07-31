import os
import pydoc
from subprocess import call

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView


from cpovc_registry.models import RegPerson, RegPersonsOrgUnits
from .models import DataQuality, Form1BServicesDataQuality


class DataQualityView(TemplateView):
    template_name = 'data_cleanup/filter.html'
    context_object_name = "data"
    filters = {}

    def get_context_data(self, **kwargs):
        context = super(
            DataQualityView, self).get_context_data(**kwargs)
        context['data'] = self.get_queryset()
        return context

    def get_final_query_set(self, model):
        user_orgs = self.request.user.reg_person.regpersonsorgunits_set.values()
        org_units = []

        for org in user_orgs:
            if not org['is_void']:
                org_units.append(org['org_unit_id'])
        return model.objects.filter(child_cbo_id__in=org_units)

    def get_queryset(self, model=DataQuality):
        return self.get_final_query_set(model)

    def set_view_filters_for_form_1b_domains(self, *args, **kwargs):
        form_1b_domain = self.request.POST.get('form_1b_domain')
        domain_filers = {}

        if form_1b_domain == '0':
            return domain_filers

        domains_map = {
            'DPSS': 'dpss',
            'DSHC': 'dshc',
            'DHES': 'dhes',
            'DEDU': 'dedu',
            'DPRO': 'dpro',
            'DHNU': 'dhnu'
        }

        for key, value in domains_map.items():
            if form_1b_domain == key:
                domain_filers[value] = True
        return domain_filers

    def post(self, *args, **kwargs):
        context = {}

        age = self.request.POST.get('age')
        age_operator = self.request.POST.get('operator')
        school_level = self.request.POST.get('school_level')
        hiv_status = self.request.POST.get('hiv_status')
        art_status = self.request.POST.get('art_status')
        gender = self.request.POST.get('gender')
        is_disabled = self.request.POST.get('is_disabled')
        is_ovc = self.request.POST.get('is_ovc')
        has_bcert = self.request.POST.get('has_bcert')
        form_1b_domain = self.request.POST.get('form_1b_domain')
        filters = {}
        if form_1b_domain:
            queryset = self.get_queryset(Form1BServicesDataQuality)
        else:
            queryset = self.get_queryset(DataQuality)

        # Maintain selected options in the views
        view_filter_values = {
            'age': age
        }

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

        if form_1b_domain and form_1b_domain != '0':
            filters['domain'] = form_1b_domain

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

        view_filter_values.update(self.set_view_filters_for_form_1b_domains())
        context['view_filter_values'] = view_filter_values
        return TemplateResponse(self.request, self.template_name, context)
