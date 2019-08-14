from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .models import (
    DataQuality, Form1BServicesDataQuality, OVCCareServicesDataQuality,
    OVCCarePriorityDataQuality, CasePlanDataQuality
)


def validate_age(age):
    """
    Validate that the age provided is a number
    """
    if isinstance(age, int):
        return True
    age_okay = True
    age_range = age.split('-')
    for number in age_range:
        try:
            int(number)
        except ValueError:
            return False
    return age_okay


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
        user_orgs = self.request.user.reg_person.regpersonsorgunits_set.values()  # noqa
        org_units = []

        for org in user_orgs:
            if not org['is_void']:
                org_units.append(org['org_unit_id'])
        return model.objects.filter(child_cbo_id__in=org_units)

    def get_queryset(self, model=DataQuality):
        if self.request.method == 'GET':
            return []
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

    def set_view_filters_for_services(self):
        service = self.request.POST.get('service')
        service_filers = {}

        if service == '0':
            return service_filers

        services_map = {
            'HC2S': 'hc2s',
            'PT2S': 'pt2s',
            'HC6S': 'hc6s',
            'CP 4s': 'cp4s',
            'SCSP': 'scsp',
            'HN 15s': 'hn15s',
            'HE1S': 'he1s',
            'HG2S': 'hg2s',
            'HN 16s': 'hn16s',
            'CP 8s': 'cp8s',
            'CE 8s': 'ce8s',
            'CP 10s': 'cp10s',
            'ES 5s': 'es5s',
            'HN 10s': 'hn10s',
            'HE3S': 'he3s',
            'CP 7s': 'cp7s',
            'HN 12s': 'hn12s',
            'HHKG': 'hhkg',
            'PS4S': 'ps4s',
            'PT3S': 'pt3s',
            'ES 3s': 'es3s',
            'HHHL': 'hhhl',
            'HC4S': 'hc4s',
            'HN 3s': 'hn3s',
            'PT1S': 'pt1s',
            'SE8S': 'se8s',
            'PS5s': 'ss5s',
            'SC3S': 'sc3s',
            'MSLG': 'mslg',
            'SC2S': 'sc25',
            'CE 11s': 'ce11s',
            'CE10s': 'ce10s',
            'MSLU': 'mslu',
            'MSNE': 'msne',
            'HAMN': 'hamn',
            'PSG4': 'psg4',
            'HE7s': 'h37s',
            'PS3S': 'ps3s',
            'HC8S': 'hc8s',
            'HN 11s': 'hn11s',
            'HN 6s': 'hn6s',
            'PS2S': 'ps2s',
            'SC6S': 'sc6s',
            'HE2S': 'he2s',
            'CP 9s': 'cp9s',
            'ES 2s': 'es2s',
            'HEG3': 'heg3',
            'HC1S': 'hc1s',
            'HN 2s': 'hn2s',
            'PS1S': 'ps1s',
            'HN 5s': 'hn5s',
            'HC7S': 'hc7s',
            'HE8s': 'h38s',
            'HC5S': 'hc5s',
            'ES 6s': 'es6s',
            'SE1S': 'se1s',
            'HN 13s': 'hn13s',
            'CP 1s': 'cp1s',
            'ES 1s': 'es1s',
            'MSLF': 'mslf',
            'CP 11s': 'cp11s',
            'HN 4s': 'hn4s',
            'PSG1': 'psg1',
            'HE5S': 'he5s',
            'SC7S': 'sc7s',
            'HC3S': 'hc3s',
            'CE9s': 'ce9s',
            'SE5S': 'se5s',
            'MSVT': 'msvt',
            'SC5S': 'sc5s',
            'PT6s': 'pt6s',
            'SE4S': 'se4s',
            'SE6S': 'se6s',
            'CE 10s': 'ce10s',
            'HNHE': 'hnhe',
            'HHHP': 'hhhp',
            'SCMM': 'scmm',
            'CE 3s': 'ce3s',
            'PPHP': 'pphp',
            'HRHC': 'hrhc',
            'PT5S': 'pt5s',
            'HCLE': 'hcle',
            'CP 5s': 'cp5s',
            'ES 7s': 'es7s',
            'CE 7s': 'ce7s',
            'HN 9s': 'hn9s',
            'MSLB': 'mslb',
            'HC10': 'hc10',
            'CE 4s': 'ce4s',
            'PT7s': 'pt7s',
            'SC1S': 'sc1s',
            'CE12s': 'ce12s',
            'MSCW': 'mscw',
            'PT4S': 'pt4s',
            'SE3S': 'se3s',
            'CE 2s': 'ce2s',
            'HG3S': 'hg3s',
            'SG1S': 'sg1s',
            'ES 4s': 'es4s',
            'CP 6s': 'cp6s',
            'CE11s': 'ce11s',
            'HRTS': 'hrts',
            'HHSU': 'hhsu',
            'MSSP': 'mssp',
            'HISF': 'hisf',
            'PHPA': 'phpa',
            'HC9S': 'hc9s',
            'HEG2': 'hegs',
            'CE 1s': 'ce1s',
            'CE 5s': 'ce5s',
            'HE6s': 'he6s',
            'PANS': 'pans',
            'SCBB': 'scbb',
            'HN 1s': 'hn1s',
            'SE9S': 'se9s',
            'PSBO': 'psbo',
            'HN 7s': 'hn7s',
            'HE4S': 'he4s',
            'HG8S': 'h58s',
            'CP12s': 'cp12s',
            'MSSL': 'mssl',
            'PHEW': 'phew',
            'HN 14s': 'hn14s',
            'CP 2s': 'cp2s',
            'CE 9s': 'ce9s',
            'HSEK': 'hsek',
            'SE2S': 'se2s',
            'SNNB': 'snnb',
            'SE7S': 'se7s',
            'HN 17s': 'hn17s',
            'SC4S': 'sc4s',
            'SNHC': 'snhc',
            'HN 8s': 'hn8s',
            'CP 3s': 'cp3s',
        }

        for key, value in services_map.items():
            if service == key:
                service_filers[value] = True
        return service_filers

    def set_view_filters_for_prorities(self):
        priority = self.request.POST.get('priority')
        priority_filters = {}

        if priority == '0':
            return priority_filters

        priorities_map = {
            'SE4S': 'priotity_se4s',
            'SE6S': 'priotity_se6s',
            'HC2S': 'priotity_hc2s',
            'PT6s': 'priotity_pt6s',
            'HNHE': 'priotity_hnhe',
            'SCMM': 'priotity_scmm',
            'HC6S': 'priotity_hc6s',
            'HE1S': 'priotity_he1s',
            'PT2S': 'priotity_pt2s',
            'SC5S': 'priotity_sc5s'
        }

        for key, value in priorities_map.items():
            if priority == key:
                priority_filters[value] = True
        return priority_filters

    def set_view_filters_for_case_plan(self):
        cp_service = self.request.POST.get('cp_service')
        cp_filters = {}

        if cp_service == '0':
            return cp_filters
        cp_service_map = {
            'CPTS7h': 'cpt57h',
            'CPTS10p': 'cpts10p',
            'CPTS5e': 'cpts5e',
            'CPTS1p': 'cpts1p',
            'CPTS6h': 'cpts6h',
            'CPTS2e': 'cpts2e',
            'CPTS6p': 'cpts6p',
            'CPTS7e': 'cpts7e',
            'CPTS5s': 'cpts5s',
            'CPTS4p': 'cpt54p',
            'CPTS7s': 'cpt57s',
            'CPTS8s': 'cpts8s',
            'CPTS3h': 'cpts3h',
            'CPTS9p': 'cpts9p',
            'CPTS10h': 'cpts10h',
            'CPTS12h': 'cpts12h',
            'CPTS1s': ' .cpts1s',
            'CPTS10e': 'cpts10e',
            'CPTS3p': 'cpts3p',
            'CPTS9h': 'cpts9h',
            'CPTS9e': 'cpts9e',
            'CPTS6s': 'cpts6s',
            'CPTS4e': 'cpts4e',
            'CPTS8e': 'cpts8e',
            'CPTS4s': 'cpts4s',
            'CPTS3e':  'cpts3e',
            'CPTS7p': 'cpts7p',
            'CPTS12p': 'cpts12p',
            'CPTS11p': 'cpts11p',
            'CPTS2s': 'cpts2s',
            'CPTS5p': 'cpts5p',
            'CPTS8p': 'cpts8p',
            'CPTS2h': 'cpts2h',
            'CPTS6e': 'cpts6e',
            'CPTS1h': 'cpts1h',
            'CPTS2p:': 'cpts2p',
            'CPTS1e': 'cpts1e',
            'CPTS4h': 'cpts4h',
            'CPTS5h': 'cpts5h',
            'CPTS11h': 'cpt511h',
            'CPTS3s': 'cpts3s',
            'CPTS8h': 'cpts8h'
        }
        for key, value in cp_service_map.items():
            if cp_service == key:
                cp_filters[value] = True
        return cp_filters

    def set_view_filters_for_ovc_exited(self):
        ovc_exited = self.request.POST.get('ovc_exited')
        ovc_exited_filters = {}

        if ovc_exited == '0':
            return ovc_exited_filters

        ovc_exited_filters_map = {
            'YES': 'ovc_exited_true',
            'NO': 'ovc_exited_false'
        }

        for key, value in ovc_exited_filters_map.items():
            if ovc_exited == key:
                ovc_exited_filters[value] = True
        return ovc_exited_filters

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
        service = self.request.POST.get('service')
        priority = self.request.POST.get('priority')
        cp_service = self.request.POST.get('cp_service')
        service_from_date = self.request.POST.get('sevice_from_date')
        service_to_date = self.request.POST.get('sevice_to_date')
        ovc_exited = self.request.POST.get('ovc_exited')
        filters = {}

        if priority and priority != '0':
            service = priority

        if form_1b_domain and form_1b_domain != '0':
            queryset = self.get_queryset(OVCCareServicesDataQuality)
        elif service and service != '0':
            queryset = self.get_queryset(OVCCareServicesDataQuality)
        elif cp_service and cp_service != '0':
            queryset = self.get_final_query_set(CasePlanDataQuality)
        else:
            queryset = self.get_final_query_set(DataQuality)

        # Maintain selected options in the views
        view_filter_values = {
            'age': age
        }

        if age:
            if not validate_age(age):
                error = 'Please provide age as numbers'
                context['error'] = error
                return TemplateResponse(
                    self.request, self.template_name, context)

            if age_operator == '-' and age_operator != '0':
                ages = age.split('-')
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
                queryset = queryset.filter(age=age)
                view_filter_values['equals'] = True
            elif age_operator == '>':
                queryset = queryset.filter(age__gt=age)
                view_filter_values['greater_than'] = True
            elif age_operator == '<':
                view_filter_values['less_than'] = True
                queryset = queryset.filter(age__lt=age)

        if ovc_exited == 'YES':
            queryset = queryset.filter(exit_date__isnull=False)
        elif ovc_exited == 'NO':
            queryset = queryset.filter(exit_date__isnull=True)

        if form_1b_domain and form_1b_domain != '0':
            filters['domain'] = form_1b_domain

        if service and service != '0':
            filters['service_provided'] = service

        if service_from_date:
            filters['date_of_event__gte'] = service_from_date

        if service_to_date:
            filters['date_of_event__lte'] = service_to_date

        if cp_service and cp_service != '0':
            filters['cp_service'] = cp_service

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
        context['data'] = queryset

        view_filter_values.update(self.set_view_filters_for_form_1b_domains())
        view_filter_values.update(self.set_view_filters_for_services())
        view_filter_values.update(self.set_view_filters_for_prorities())
        view_filter_values.update(self.set_view_filters_for_case_plan())
        view_filter_values.update(self.set_view_filters_for_ovc_exited())
        context['view_filter_values'] = view_filter_values
        return TemplateResponse(self.request, self.template_name, context)


class CasePlanDataQualityView(DataQualityView):
        template_name = 'data_cleanup/case_plan_filter.html'
