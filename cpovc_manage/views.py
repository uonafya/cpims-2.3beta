import collections
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import NOTTTravel, NOTTChaperon, NOTTChild, OvcCasePersons
from .forms import NOTTForm, ChaperonForm, ChildrenForm
from cpovc_main.functions import convert_date
from django.forms.models import model_to_dict
from cpovc_forms.models import OVCBasicCRS, OVCBasicCategory, OVCBasicPerson
from cpovc_registry.models import RegPerson, RegPersonsExternalIds
from cpovc_settings.functions import get_geo
from cpovc_main.functions import get_dict
from .functions import travel_pdf


@login_required(login_url='/')
def manage_home(request):
    """Main home method and view."""
    try:
        return render(request, 'management/home.html',
                      {'form': {}})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def home_travel(request):
    """Main home method and view."""
    try:
        if request.method == 'POST':
            dts, vals = {}, {}
            dtls = ['is_void', 'sync_id', 'id']
            item_id = request.POST.get('item_id')
            data = NOTTTravel.objects.filter(
                is_void=False, pk=item_id).values()[0]
            for dt in data:
                if data[dt] is not None and data[dt] != '' and dt not in dtls:
                    dval = vals[data[dt]] if data[dt] in vals else data[dt]
                    if isinstance(dval, (bool)):
                        dval = 'Yes' if dval else 'No'
                    dts[dt.replace('_', ' ').capitalize()] = dval
            datas = collections.OrderedDict(sorted(dts.items()))
            results = {'message': 'Good', 'status': 0, 'dates': '0000',
                       'data': datas}
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        cases = NOTTTravel.objects.filter(is_void=False)
        return render(request, 'management/home_travel.html',
                      {'form': {}, 'cases': cases})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def new_travel(request):
    """Main home method and view."""
    try:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            print(item_id)
        return render(request, 'management/edit_travel.html',
                      {'form': {}})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def view_travel(request, id):
    """Main home method and view."""
    try:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            print(item_id)
        travel = NOTTTravel.objects.get(is_void=False, id=id)
        chaperons = NOTTChaperon.objects.filter(travel_id=id)
        children = NOTTChild.objects.filter(travel_id=id)
        return render(request, 'management/view_travel.html',
                      {'form': {}, 'travel': travel,
                       'chaperons': chaperons, 'children': children})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def travel_report(request, id):
    """Main home method and view."""
    try:
        file_name = 'National_Travel-Authorization_%s' % (id)
        fname = '%s.pdf' % (file_name)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (fname)
        travel_pdf(request, response, file_name)
        return response
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def edit_travel(request, id):
    """Main home method and view."""
    try:
        ChaperonFormset = formset_factory(ChaperonForm, extra=0)
        ChildrenFormset = formset_factory(ChildrenForm, extra=0)
        if request.method == 'POST':
            travel = NOTTTravel.objects.get(is_void=False, id=id)
            tdate = request.POST.get('travel_date')
            return_date = request.POST.get('return_date')
            no_applied = request.POST.get('no_applied')
            no_cleared = request.POST.get('no_cleared')
            no_returned = request.POST.get('no_returned')
            comments = request.POST.get('comments')
            contacts = request.POST.get('contacts')
            sponsor = request.POST.get('sponsor')
            reason = request.POST.get('reason')
            status_id = request.POST.get('status')
            status = 1 if status_id == 'on' else 0
            institution_name = request.POST.get('institution_name')
            country_name = request.POST.get('country_name')
            travel_date = convert_date(tdate)
            if return_date:
                return_date = convert_date(return_date)
            travel.travel_date = travel_date
            travel.return_date = return_date
            travel.contacts = contacts
            travel.comments = comments
            travel.sponsor = sponsor
            travel.reason = reason
            travel.status = status
            travel.institution_name = institution_name
            travel.country_name = country_name
            # travel.save()
            # Chaperon
            formset = ChaperonFormset(request.POST, prefix='chap')
            cformset = ChildrenFormset(request.POST, prefix='child')
            print(request.POST)
            clear_count, return_count = 0, 0
            if formset.is_valid():
                if formset.has_changed():
                    for echap in formset.cleaned_data:
                        ops = OvcCasePersons.objects.get(pk=echap['person_id'])
                        ops.person_sex = echap['sex']
                        ops.person_first_name = echap['first_name']
                        ops.person_other_names = echap['other_names']
                        ops.person_surname = echap['surname']
                        ops.person_identifier = echap['passport_no']
                        ops.save()
            else:
                print(formset.errors)
            if cformset.is_valid():
                if cformset.has_changed():
                    no_applied = len(cformset.cleaned_data)
                    for echild in cformset.cleaned_data:
                        cid = echild['person_id']
                        cidc = echild['cleared']
                        cidr = echild['returned']
                        cid_cleared = True if cidc == 'True' else False
                        cid_returned = True if cidr == 'True' else False
                        if cid_cleared:
                            clear_count += 1
                        if cid_returned:
                            return_count += 1
                        opc = RegPerson.objects.get(pk=cid)
                        opc.sex_id = echild['sex']
                        opc.first_name = echild['first_name']
                        opc.other_names = echild['other_names']
                        opc.surname = echild['surname']
                        opc.save()
                        # Update passport Number
                        cpp = RegPersonsExternalIds.objects.get(
                            person_id=cid, is_void=False,
                            identifier_type_id='IPPN')
                        cpp.identifier = echild['passport_no']
                        cpp.save()
                        # Update Returned / Cleared details
                        ch = NOTTChild.objects.get(travel_id=id, person_id=cid)
                        ch.returned = cid_returned
                        ch.cleared = cid_cleared
                        ch.save()
                        print(echild)
                    no_returned = return_count
                    no_cleared = clear_count
            else:
                print(cformset.errors)
            travel.no_applied = no_applied
            travel.no_cleared = no_cleared
            travel.no_returned = no_returned
            travel.save()
            url = reverse(view_travel, kwargs={'id': id})
            return HttpResponseRedirect(url)
        travel = NOTTTravel.objects.filter(is_void=False, id=id).values()[0]
        travel_date = travel['travel_date'].strftime('%d-%b-%Y')
        return_date = None
        if travel['return_date']:
            return_date = travel['return_date'].strftime('%d-%b-%Y')
        travel['travel_date'] = travel_date
        travel['return_date'] = return_date
        nott_form = NOTTForm(travel)
        # Chaperons
        chaps = []
        chaperons = NOTTChaperon.objects.filter(travel_id=id)
        for chap in chaperons:
            chap_details = {'first_name': chap.other_person.person_first_name}
            chap_details['surname'] = chap.other_person.person_surname
            chap_details['other_names'] = chap.other_person.person_other_names
            chap_details['sex'] = chap.other_person.person_sex
            chap_details['passport_no'] = chap.other_person.person_identifier
            chap_details['person_id'] = chap.other_person_id
            chap_details['chaperon_id'] = chap.id
            chaps.append(chap_details)
        chap_formset = ChaperonFormset(initial=chaps, prefix='chap')
        # Children
        tchildren = []
        children = NOTTChild.objects.filter(travel_id=id)
        for child in children:
            child_details = {'first_name': child.person.first_name}
            child_details['surname'] = child.person.surname
            child_details['other_names'] = child.person.other_names
            child_details['sex'] = child.person.sex_id
            child_details['passport_no'] = child.passport
            child_details['person_id'] = child.person_id
            child_details['child_id'] = child.id
            child_details['cleared'] = child.cleared
            child_details['returned'] = child.returned
            tchildren.append(child_details)
        child_formset = ChildrenFormset(initial=tchildren, prefix='child')
        return render(request, 'management/edit_travel.html',
                      {'form': nott_form, 'travel': travel,
                       'chap_formset': chap_formset,
                       'child_formset': child_formset})
    except Exception as e:
        raise e
    else:
        pass


# Create your views here.
@login_required
def integration_home(request):
    """Method to do pivot reports."""
    try:
        persons = {}
        categories = {}
        case_data = {}
        rm_fields = ['is_void', 'account', 'case_serial']
        check_fields = ['sex_id', 'case_category_id', 'case_reporter_id',
                        'family_status_id', 'household_economics',
                        'risk_level_id', 'mental_condition_id',
                        'perpetrator_status_id', 'other_condition_id',
                        'physical_condition_id', 'yesno_id']
        vals = get_dict(field_name=check_fields)
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            case = OVCBasicCRS.objects.get(
                case_id=item_id, is_void=False)
            cdata = model_to_dict(case)
            for cd in cdata:
                cdt = cdata[cd]
                if len(str(cdt)) < 6 and cdt in vals:
                    cdt = vals[cdt]
                if cdt and cd not in rm_fields:
                    case_data[cd] = cdt
                if cdt and (cd == 'county' or cd == 'constituency'):
                    cd_name = '%s name' % (cd)
                    case_data[cd_name] = get_geo(cdt)
            results = {'status': 0, 'message': 'Successful', 'dates': '',
                       'data': case_data}
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        cases = OVCBasicCRS.objects.filter(
            is_void=False).order_by('-timestamp_created')
        case_cats = OVCBasicCategory.objects.filter(is_void=False)
        case_pers = OVCBasicPerson.objects.filter(is_void=False)
        for ccat in case_cats:
            categories[ccat.case_id] = ccat
        for cpers in case_pers:
            pers_type = cpers.person_type
            if pers_type == 'PTCH':
                persons[cpers.case_id] = cpers
        for c in cases:
            cid = c.case_id
            category = categories[cid] if cid in categories else None
            child = persons[cid] if cid in persons else None
            setattr(c, 'category', category)
            setattr(c, 'child', child)
        return render(request, 'management/integration.html',
                      {'form': {}, 'cases': cases, 'vals': vals})
    except Exception as e:
        print(e)
        raise e
    else:
        pass
