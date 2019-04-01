"""CPIMS GIS module."""
from random import randint
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def gis_home(request):
    """Method for gis."""
    try:
        return render(request, 'gis/gis_home.html')
    except Exception, e:
        raise e


def random_data(aid):
    """Random data sets."""
    data = {}
    pop_data = randint(0, 120)
    data[0] = ["Cases", pop_data]
    data[1] = ["Postal Address", "BOX xxxx - 00200 Nairobi"]
    data[2] = ["Contact Person", "Mrs Contact Person"]
    data[3] = ["Telephone number", "2547000123123"]
    data[4] = ["Physical Address", "Ngong Road Opposite xyz"]
    return data[aid]


def gis_data(request):
    """Method for gis to get sample data."""
    try:
        results = []
        category_id = request.GET.get('category')
        region_id = int(request.GET.get('region'))
        action_id = int(request.GET.get('action'))
        region_type = 'COUNTY' if region_id == 1 else 'SUB_COUNTY'
        results.append(["CPIMS_%s" % (category_id), region_type])
        if action_id == 2:
            rid = randint(0, 5)
            a_name = "Org Unit " if int(category_id) == 1 else region_type
            pop_data = randint(0, 120)
            values = ["%s Population" % (a_name), pop_data]
            results.append(values)
            if int(category_id) > 1:
                rid = 0
            results.append(random_data(rid))
        else:
            upper_limit = 47 if region_id == 1 else 290
            for var in range(1, upper_limit + 1):
                cp_data = randint(0, 120)
                cp_val = [cp_data, var]
                results.append(cp_val)
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception, e:
        raise e
